"""
AUTHENTICATION SYSTEM - Consciousness Platform
================================================
JWT-based authentication with OAuth 2.0 support (Google/GitHub).

Work Order: WO-006
Created: 2025-11-27
"""

import os
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from typing import Optional, Dict, Any
from authlib.integrations.flask_client import OAuth

# Configuration
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "change-this-secret-key-in-production")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_HOURS = int(os.environ.get("JWT_EXPIRATION_HOURS", "24"))
REFRESH_TOKEN_EXPIRATION_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRATION_DAYS", "30"))

# OAuth Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET")

# Initialize OAuth
oauth = OAuth()

# Configure Google OAuth
if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

# Configure GitHub OAuth
if GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET:
    oauth.register(
        name='github',
        client_id=GITHUB_CLIENT_ID,
        client_secret=GITHUB_CLIENT_SECRET,
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize',
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'}
    )


# ============= Token Management =============

def create_access_token(user_id: int, email: str) -> str:
    """Create JWT access token"""
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow(),
        'type': 'access'
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_refresh_token(user_id: int) -> str:
    """Create JWT refresh token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRATION_DAYS),
        'iat': datetime.utcnow(),
        'type': 'refresh'
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token


def get_token_from_header() -> Optional[str]:
    """Extract token from Authorization header"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None

    # Expected format: "Bearer <token>"
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None

    return parts[1]


# ============= Authentication Decorators =============

def token_required(f):
    """Decorator to protect routes - requires valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_from_header()

        if not token:
            return jsonify({'error': 'Missing authentication token'}), 401

        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401

        if payload.get('type') != 'access':
            return jsonify({'error': 'Invalid token type'}), 401

        # Add user info to request context
        request.current_user_id = payload.get('user_id')
        request.current_user_email = payload.get('email')

        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    """Decorator to protect admin routes"""
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        from models import User, SessionLocal

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == request.current_user_id).first()
            if not user or not user.is_admin:
                return jsonify({'error': 'Admin access required'}), 403

            return f(*args, **kwargs)
        finally:
            db.close()

    return decorated


def subscription_required(tier: str):
    """Decorator to require specific subscription tier"""
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated(*args, **kwargs):
            from models import User, SessionLocal

            # Tier hierarchy: free < pro < enterprise
            tier_levels = {'free': 0, 'pro': 1, 'enterprise': 2}
            required_level = tier_levels.get(tier, 0)

            db = SessionLocal()
            try:
                user = db.query(User).filter(User.id == request.current_user_id).first()
                if not user:
                    return jsonify({'error': 'User not found'}), 404

                user_level = tier_levels.get(user.subscription_tier, 0)
                if user_level < required_level:
                    return jsonify({
                        'error': 'Subscription upgrade required',
                        'required_tier': tier,
                        'current_tier': user.subscription_tier
                    }), 403

                return f(*args, **kwargs)
            finally:
                db.close()

        return decorated
    return decorator


# ============= Password Utilities =============

def validate_password(password: str) -> tuple[bool, Optional[str]]:
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"

    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"

    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"

    return True, None


# ============= Email Validation =============

def validate_email(email: str) -> bool:
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# ============= User Registration =============

def register_user(email: str, password: str, full_name: Optional[str] = None) -> tuple[bool, Any]:
    """
    Register new user with email/password.

    Returns: (success, result)
    - If success: (True, user_object)
    - If failure: (False, error_message)
    """
    from models import User, SessionLocal

    # Validate email
    if not validate_email(email):
        return False, "Invalid email format"

    # Validate password
    valid, error = validate_password(password)
    if not valid:
        return False, error

    db = SessionLocal()
    try:
        # Check if email exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            return False, "Email already registered"

        # Create user
        user = User(
            email=email,
            full_name=full_name,
            subscription_tier='free',
            is_active=True
        )
        user.set_password(password)

        db.add(user)
        db.commit()
        db.refresh(user)

        return True, user

    except Exception as e:
        db.rollback()
        return False, f"Registration failed: {str(e)}"

    finally:
        db.close()


# ============= User Login =============

def authenticate_user(email: str, password: str) -> tuple[bool, Any]:
    """
    Authenticate user with email/password.

    Returns: (success, result)
    - If success: (True, user_object)
    - If failure: (False, error_message)
    """
    from models import User, SessionLocal

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()

        if not user:
            return False, "Invalid email or password"

        if not user.is_active:
            return False, "Account is disabled"

        if not user.check_password(password):
            return False, "Invalid email or password"

        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()

        return True, user

    finally:
        db.close()


# ============= OAuth Handlers =============

def create_or_update_oauth_user(provider: str, oauth_id: str, email: str,
                                 full_name: Optional[str] = None,
                                 avatar_url: Optional[str] = None) -> tuple[bool, Any]:
    """
    Create or update user from OAuth provider.

    Returns: (success, result)
    """
    from models import User, SessionLocal

    db = SessionLocal()
    try:
        # Check if user exists with this OAuth ID
        if provider == 'google':
            user = db.query(User).filter(User.google_id == oauth_id).first()
        elif provider == 'github':
            user = db.query(User).filter(User.github_id == oauth_id).first()
        else:
            return False, f"Unknown provider: {provider}"

        if user:
            # Update existing user
            user.last_login = datetime.utcnow()
            if full_name:
                user.full_name = full_name
            if avatar_url:
                user.avatar_url = avatar_url
        else:
            # Check if email exists
            user = db.query(User).filter(User.email == email).first()

            if user:
                # Link OAuth to existing account
                if provider == 'google':
                    user.google_id = oauth_id
                elif provider == 'github':
                    user.github_id = oauth_id
            else:
                # Create new user
                user = User(
                    email=email,
                    full_name=full_name,
                    avatar_url=avatar_url,
                    subscription_tier='free',
                    is_active=True
                )
                if provider == 'google':
                    user.google_id = oauth_id
                elif provider == 'github':
                    user.github_id = oauth_id

                db.add(user)

            user.last_login = datetime.utcnow()

        db.commit()
        db.refresh(user)

        return True, user

    except Exception as e:
        db.rollback()
        return False, f"OAuth authentication failed: {str(e)}"

    finally:
        db.close()


# ============= Utilities =============

def get_current_user():
    """Get current authenticated user from request context"""
    from models import User, SessionLocal

    if not hasattr(request, 'current_user_id'):
        return None

    db = SessionLocal()
    try:
        return db.query(User).filter(User.id == request.current_user_id).first()
    finally:
        db.close()


# ============= Main (for testing) =============

if __name__ == "__main__":
    print("=" * 60)
    print("AUTHENTICATION SYSTEM - Consciousness Platform")
    print("=" * 60)
    print("\nFeatures:")
    print("  ✅ JWT access tokens (24hr expiration)")
    print("  ✅ JWT refresh tokens (30 day expiration)")
    print("  ✅ Password hashing (werkzeug)")
    print("  ✅ OAuth 2.0 (Google + GitHub)")
    print("  ✅ Protected route decorators (@token_required)")
    print("  ✅ Subscription tier enforcement")
    print("  ✅ Admin role checking")
    print("\nDecorators:")
    print("  @token_required - Require authentication")
    print("  @admin_required - Require admin role")
    print("  @subscription_required('pro') - Require subscription tier")
    print("\nFunctions:")
    print("  register_user(email, password)")
    print("  authenticate_user(email, password)")
    print("  create_access_token(user_id, email)")
    print("  create_refresh_token(user_id)")
    print("  get_current_user()")
    print("=" * 60)
