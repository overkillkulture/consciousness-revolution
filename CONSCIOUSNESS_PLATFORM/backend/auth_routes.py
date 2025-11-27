"""
AUTHENTICATION ROUTES - Consciousness Platform
================================================
API endpoints for user authentication, registration, and OAuth.

Work Order: WO-006
Created: 2025-11-27
"""

from flask import Blueprint, request, jsonify, redirect, url_for, session
from auth import (
    register_user,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token,
    token_required,
    get_current_user,
    oauth,
    create_or_update_oauth_user
)
from models import User, SessionLocal

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


# ============= Registration & Login =============

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    Register new user account.

    Request body:
    {
        "email": "user@example.com",
        "password": "SecurePass123",
        "full_name": "John Doe" (optional)
    }

    Response:
    {
        "success": true,
        "user": {...},
        "access_token": "...",
        "refresh_token": "..."
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Missing request body'}), 400

        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')

        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400

        # Register user
        success, result = register_user(email, password, full_name)

        if not success:
            return jsonify({'error': result}), 400

        user = result

        # Generate tokens
        access_token = create_access_token(user.id, user.email)
        refresh_token = create_refresh_token(user.id)

        return jsonify({
            'success': True,
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login with email and password.

    Request body:
    {
        "email": "user@example.com",
        "password": "SecurePass123"
    }

    Response:
    {
        "success": true,
        "user": {...},
        "access_token": "...",
        "refresh_token": "..."
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Missing request body'}), 400

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400

        # Authenticate user
        success, result = authenticate_user(email, password)

        if not success:
            return jsonify({'error': result}), 401

        user = result

        # Generate tokens
        access_token = create_access_token(user.id, user.email)
        refresh_token = create_refresh_token(user.id)

        return jsonify({
            'success': True,
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """
    Refresh access token using refresh token.

    Request body:
    {
        "refresh_token": "..."
    }

    Response:
    {
        "success": true,
        "access_token": "..."
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Missing request body'}), 400

        refresh_token = data.get('refresh_token')

        if not refresh_token:
            return jsonify({'error': 'Refresh token required'}), 400

        # Decode refresh token
        payload = decode_token(refresh_token)

        if not payload:
            return jsonify({'error': 'Invalid or expired refresh token'}), 401

        if payload.get('type') != 'refresh':
            return jsonify({'error': 'Invalid token type'}), 401

        # Get user
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == payload.get('user_id')).first()

            if not user or not user.is_active:
                return jsonify({'error': 'User not found or inactive'}), 401

            # Generate new access token
            access_token = create_access_token(user.id, user.email)

            return jsonify({
                'success': True,
                'access_token': access_token
            })

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= Current User =============

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_me():
    """
    Get current authenticated user info.

    Headers:
        Authorization: Bearer <access_token>

    Response:
    {
        "success": true,
        "user": {...}
    }
    """
    try:
        user = get_current_user()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'success': True,
            'user': user.to_dict()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= OAuth - Google =============

@auth_bp.route('/oauth/google')
def google_login():
    """Initiate Google OAuth flow"""
    if not oauth.google:
        return jsonify({'error': 'Google OAuth not configured'}), 503

    redirect_uri = url_for('auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth_bp.route('/oauth/google/callback')
def google_callback():
    """Google OAuth callback"""
    if not oauth.google:
        return jsonify({'error': 'Google OAuth not configured'}), 503

    try:
        # Get token from Google
        token = oauth.google.authorize_access_token()

        # Get user info from Google
        user_info = token.get('userinfo')

        if not user_info:
            return jsonify({'error': 'Failed to get user info from Google'}), 400

        google_id = user_info.get('sub')
        email = user_info.get('email')
        full_name = user_info.get('name')
        avatar_url = user_info.get('picture')

        if not google_id or not email:
            return jsonify({'error': 'Incomplete user info from Google'}), 400

        # Create or update user
        success, result = create_or_update_oauth_user(
            'google', google_id, email, full_name, avatar_url
        )

        if not success:
            return jsonify({'error': result}), 400

        user = result

        # Generate tokens
        access_token = create_access_token(user.id, user.email)
        refresh_token = create_refresh_token(user.id)

        # Store in session for redirect
        session['access_token'] = access_token
        session['refresh_token'] = refresh_token

        # Redirect to frontend with tokens
        frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
        return redirect(f"{frontend_url}/auth/callback?access_token={access_token}&refresh_token={refresh_token}")

    except Exception as e:
        return jsonify({'error': f'Google OAuth failed: {str(e)}'}), 500


# ============= OAuth - GitHub =============

@auth_bp.route('/oauth/github')
def github_login():
    """Initiate GitHub OAuth flow"""
    if not oauth.github:
        return jsonify({'error': 'GitHub OAuth not configured'}), 503

    redirect_uri = url_for('auth.github_callback', _external=True)
    return oauth.github.authorize_redirect(redirect_uri)


@auth_bp.route('/oauth/github/callback')
def github_callback():
    """GitHub OAuth callback"""
    if not oauth.github:
        return jsonify({'error': 'GitHub OAuth not configured'}), 503

    try:
        # Get token from GitHub
        token = oauth.github.authorize_access_token()

        # Get user info from GitHub
        resp = oauth.github.get('user', token=token)
        user_info = resp.json()

        if not user_info:
            return jsonify({'error': 'Failed to get user info from GitHub'}), 400

        github_id = str(user_info.get('id'))
        email = user_info.get('email')
        full_name = user_info.get('name')
        avatar_url = user_info.get('avatar_url')

        # If email is private, get it from emails endpoint
        if not email:
            emails_resp = oauth.github.get('user/emails', token=token)
            emails = emails_resp.json()
            primary_email = next((e for e in emails if e.get('primary')), None)
            if primary_email:
                email = primary_email.get('email')

        if not github_id or not email:
            return jsonify({'error': 'Incomplete user info from GitHub'}), 400

        # Create or update user
        success, result = create_or_update_oauth_user(
            'github', github_id, email, full_name, avatar_url
        )

        if not success:
            return jsonify({'error': result}), 400

        user = result

        # Generate tokens
        access_token = create_access_token(user.id, user.email)
        refresh_token = create_refresh_token(user.id)

        # Store in session for redirect
        session['access_token'] = access_token
        session['refresh_token'] = refresh_token

        # Redirect to frontend with tokens
        frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
        return redirect(f"{frontend_url}/auth/callback?access_token={access_token}&refresh_token={refresh_token}")

    except Exception as e:
        return jsonify({'error': f'GitHub OAuth failed: {str(e)}'}), 500


# ============= Password Management =============

@auth_bp.route('/change-password', methods=['POST'])
@token_required
def change_password():
    """
    Change password for authenticated user.

    Headers:
        Authorization: Bearer <access_token>

    Request body:
    {
        "current_password": "OldPass123",
        "new_password": "NewPass456"
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Missing request body'}), 400

        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not current_password or not new_password:
            return jsonify({'error': 'Current and new password required'}), 400

        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Verify current password
        if not user.check_password(current_password):
            return jsonify({'error': 'Invalid current password'}), 401

        # Validate new password
        from auth import validate_password
        valid, error = validate_password(new_password)
        if not valid:
            return jsonify({'error': error}), 400

        # Update password
        db = SessionLocal()
        try:
            user.set_password(new_password)
            db.commit()

            return jsonify({
                'success': True,
                'message': 'Password updated successfully'
            })

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= Account Deletion =============

@auth_bp.route('/delete-account', methods=['DELETE'])
@token_required
def delete_account():
    """
    Delete authenticated user account.

    Headers:
        Authorization: Bearer <access_token>

    Request body:
    {
        "password": "CurrentPass123",
        "confirm": true
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Missing request body'}), 400

        password = data.get('password')
        confirm = data.get('confirm')

        if not password or not confirm:
            return jsonify({'error': 'Password and confirmation required'}), 400

        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Verify password
        if not user.check_password(password):
            return jsonify({'error': 'Invalid password'}), 401

        # Delete user (cascade will delete related records)
        db = SessionLocal()
        try:
            db.delete(user)
            db.commit()

            return jsonify({
                'success': True,
                'message': 'Account deleted successfully'
            })

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= Utilities =============

import os  # Add at top if not present

def init_oauth(app):
    """Initialize OAuth with Flask app"""
    oauth.init_app(app)
