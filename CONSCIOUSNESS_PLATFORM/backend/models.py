"""
DATABASE MODELS - Consciousness Platform
==========================================
SQLAlchemy models for user management, assessments, subscriptions, and platform data.

Created: 2025-11-27
Work Order: WO-005
"""

import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from werkzeug.security import generate_password_hash, check_password_hash

# Database setup
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost:5432/consciousness_platform")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ============= User Management =============

class User(Base):
    """User account model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)  # Null for OAuth-only users

    # Profile
    username = Column(String(100), unique=True, nullable=True)
    full_name = Column(String(255), nullable=True)
    avatar_url = Column(String(500), nullable=True)

    # Subscription
    subscription_tier = Column(String(50), default="free")  # free, pro, enterprise
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    # OAuth
    google_id = Column(String(255), unique=True, nullable=True)
    github_id = Column(String(255), unique=True, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    assessments = relationship("Assessment", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    course_progress = relationship("CourseProgress", back_populates="user", cascade="all, delete-orphan")
    forum_posts = relationship("ForumPost", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password: str):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify password"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "avatar_url": self.avatar_url,
            "subscription_tier": self.subscription_tier,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None
        }


# ============= Assessments =============

class Assessment(Base):
    """Consciousness Bridge assessment results"""
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Results
    consciousness_level = Column(Float, nullable=False)  # 0-1000 scale
    level_name = Column(String(100), nullable=False)  # Asleep, Awakening, etc.
    percentile = Column(Integer, nullable=False)  # 1-99

    # Domain scores (JSON)
    domain_scores = Column(JSON, nullable=False)  # {"physical": 0.75, "financial": 0.82, ...}
    strengths = Column(JSON, nullable=False)  # List of strength areas
    growth_areas = Column(JSON, nullable=False)  # List of growth opportunities
    recommended_path = Column(Text, nullable=True)

    # Raw answers (for analytics)
    raw_answers = Column(JSON, nullable=True)  # {"1": 2, "2": 1, ...}

    # Metadata
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6

    # Relationships
    user = relationship("User", back_populates="assessments")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "consciousness_level": self.consciousness_level,
            "level_name": self.level_name,
            "percentile": self.percentile,
            "domain_scores": self.domain_scores,
            "strengths": self.strengths,
            "growth_areas": self.growth_areas,
            "recommended_path": self.recommended_path,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


# ============= Subscriptions =============

class Subscription(Base):
    """Stripe subscription records"""
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Stripe data
    stripe_customer_id = Column(String(255), unique=True, nullable=False)
    stripe_subscription_id = Column(String(255), unique=True, nullable=True)
    stripe_price_id = Column(String(255), nullable=True)

    # Subscription info
    plan = Column(String(50), nullable=False)  # free, pro, enterprise
    status = Column(String(50), nullable=False)  # active, canceled, past_due, etc.

    # Billing
    current_period_start = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)
    cancel_at_period_end = Column(Boolean, default=False)
    canceled_at = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="subscriptions")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "plan": self.plan,
            "status": self.status,
            "current_period_end": self.current_period_end.isoformat() if self.current_period_end else None,
            "cancel_at_period_end": self.cancel_at_period_end,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


# ============= Course Progress =============

class CourseProgress(Base):
    """Track user progress through Pattern Theory Academy"""
    __tablename__ = "course_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Course identification
    course_id = Column(String(100), nullable=False, index=True)  # e.g., "pattern-theory-101"
    lesson_id = Column(String(100), nullable=False, index=True)  # e.g., "lesson-3-manipulation"

    # Progress
    completed = Column(Boolean, default=False)
    progress_percent = Column(Integer, default=0)  # 0-100

    # Tracking
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    last_accessed = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Lesson data (quiz scores, etc.)
    lesson_data = Column(JSON, nullable=True)  # {"quiz_score": 0.85, "attempts": 2, ...}

    # Relationships
    user = relationship("User", back_populates="course_progress")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "course_id": self.course_id,
            "lesson_id": self.lesson_id,
            "completed": self.completed,
            "progress_percent": self.progress_percent,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


# ============= Forum/Community =============

class ForumPost(Base):
    """Community forum posts and discussions"""
    __tablename__ = "forum_posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Post content
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)  # discussion, success-story, question, etc.

    # Threading (for replies)
    parent_id = Column(Integer, ForeignKey("forum_posts.id"), nullable=True, index=True)

    # Engagement
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    view_count = Column(Integer, default=0)

    # Moderation
    is_pinned = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="forum_posts")
    replies = relationship("ForumPost",
                          backref="parent",
                          remote_side=[id],
                          cascade="all, delete-orphan")

    def to_dict(self, include_content=True):
        """Convert to dictionary"""
        result = {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "category": self.category,
            "parent_id": self.parent_id,
            "upvotes": self.upvotes,
            "downvotes": self.downvotes,
            "view_count": self.view_count,
            "is_pinned": self.is_pinned,
            "is_locked": self.is_locked,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        if include_content:
            result["content"] = self.content
        return result


# ============= Helper Functions =============

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")


def get_db():
    """Get database session (for FastAPI dependency injection)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============= Main =============

if __name__ == "__main__":
    print("=" * 60)
    print("CONSCIOUSNESS PLATFORM - DATABASE MODELS")
    print("=" * 60)
    print(f"Database URL: {DATABASE_URL}")
    print("\nModels defined:")
    print("  - User (authentication & profiles)")
    print("  - Assessment (consciousness bridge results)")
    print("  - Subscription (Stripe billing)")
    print("  - CourseProgress (academy tracking)")
    print("  - ForumPost (community discussions)")
    print("\nTo initialize database:")
    print("  python models.py")
    print("\nTo create migrations:")
    print("  alembic revision --autogenerate -m 'Initial migration'")
    print("  alembic upgrade head")
    print("=" * 60)

    # Create tables
    choice = input("\nCreate database tables now? (y/n): ")
    if choice.lower() == 'y':
        init_db()
