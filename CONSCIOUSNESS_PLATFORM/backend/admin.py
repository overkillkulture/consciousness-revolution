"""
ADMIN DASHBOARD API - Platform Management System
=================================================
Administrative endpoints for user management, content moderation, and analytics.

Work Order: Build 9 - Admin Dashboard API
Created: 2025-11-27

IMPORTANT: All endpoints require admin authentication (@admin_required).
"""

import os
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from sqlalchemy import func, and_, or_, desc
from auth import token_required, admin_required, get_current_user
from models import User, ForumPost, CourseProgress, AssessmentResult, Payment, SessionLocal

# Create admin blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')


# ============= USER MANAGEMENT =============

@admin_bp.route('/users', methods=['GET'])
@token_required
@admin_required
def list_users():
    """
    List all users with filtering and pagination.

    Query params:
    - search: Search by email or name
    - role: Filter by role (user/admin)
    - subscription: Filter by subscription tier (free/pro/enterprise)
    - banned: Filter by banned status (true/false)
    - limit: Results per page (default 50)
    - offset: Pagination offset (default 0)
    - sort_by: Sort field (created_at, email, subscription_tier)
    - sort_order: Sort direction (asc/desc, default desc)
    """
    db = SessionLocal()
    try:
        # Get query parameters
        search = request.args.get('search', '').strip()
        role = request.args.get('role')
        subscription = request.args.get('subscription')
        banned_filter = request.args.get('banned')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')

        # Build query
        query = db.query(User)

        # Apply filters
        if search:
            search_pattern = f'%{search}%'
            query = query.filter(
                or_(
                    User.email.ilike(search_pattern),
                    User.name.ilike(search_pattern)
                )
            )

        if role:
            query = query.filter(User.is_admin == (role == 'admin'))

        if subscription:
            query = query.filter(User.subscription_tier == subscription)

        if banned_filter:
            is_banned = banned_filter.lower() == 'true'
            query = query.filter(User.is_banned == is_banned)

        # Get total count before pagination
        total_count = query.count()

        # Apply sorting
        sort_column = getattr(User, sort_by, User.created_at)
        if sort_order == 'desc':
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(sort_column)

        # Apply pagination
        users = query.limit(limit).offset(offset).all()

        # Format response
        users_data = []
        for user in users:
            users_data.append({
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'is_admin': user.is_admin,
                'is_banned': user.is_banned,
                'subscription_tier': user.subscription_tier,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'last_login': user.last_login.isoformat() if user.last_login else None
            })

        return jsonify({
            'success': True,
            'users': users_data,
            'total': total_count,
            'limit': limit,
            'offset': offset
        })

    finally:
        db.close()


@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
@admin_required
def get_user_details(user_id):
    """Get detailed information about a specific user."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get user statistics
        course_count = db.query(CourseProgress).filter(
            CourseProgress.user_id == user_id
        ).count()

        completed_courses = db.query(CourseProgress).filter(
            and_(
                CourseProgress.user_id == user_id,
                CourseProgress.completed == True
            )
        ).count()

        forum_posts = db.query(ForumPost).filter(
            and_(
                ForumPost.user_id == user_id,
                ForumPost.is_deleted == False
            )
        ).count()

        total_payments = db.query(func.sum(Payment.amount)).filter(
            and_(
                Payment.user_id == user_id,
                Payment.status == 'succeeded'
            )
        ).scalar() or 0

        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'is_admin': user.is_admin,
                'is_banned': user.is_banned,
                'subscription_tier': user.subscription_tier,
                'stripe_customer_id': user.stripe_customer_id,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'statistics': {
                    'courses_started': course_count,
                    'courses_completed': completed_courses,
                    'forum_posts': forum_posts,
                    'total_revenue': total_payments / 100  # Convert cents to dollars
                }
            }
        })

    finally:
        db.close()


@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@token_required
@admin_required
def update_user_role(user_id):
    """
    Update user role (promote to admin or demote to user).

    Request body:
    {
        "is_admin": true/false
    }
    """
    data = request.get_json()
    is_admin = data.get('is_admin')

    if is_admin is None:
        return jsonify({'error': 'is_admin field required'}), 400

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Prevent admin from removing their own admin status
        current_user = get_current_user()
        if user.id == current_user.id and not is_admin:
            return jsonify({'error': 'Cannot remove your own admin privileges'}), 403

        user.is_admin = is_admin
        db.commit()

        action = 'promoted to admin' if is_admin else 'demoted to user'
        return jsonify({
            'success': True,
            'message': f'User {action}',
            'user': {
                'id': user.id,
                'email': user.email,
                'is_admin': user.is_admin
            }
        })

    finally:
        db.close()


@admin_bp.route('/users/<int:user_id>/ban', methods=['PUT'])
@token_required
@admin_required
def ban_user(user_id):
    """
    Ban or unban a user.

    Request body:
    {
        "banned": true/false,
        "reason": "Optional ban reason"
    }
    """
    data = request.get_json()
    banned = data.get('banned')
    reason = data.get('reason', '')

    if banned is None:
        return jsonify({'error': 'banned field required'}), 400

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Prevent admin from banning themselves
        current_user = get_current_user()
        if user.id == current_user.id:
            return jsonify({'error': 'Cannot ban yourself'}), 403

        # Prevent banning other admins
        if user.is_admin:
            return jsonify({'error': 'Cannot ban admin users'}), 403

        user.is_banned = banned
        db.commit()

        action = 'banned' if banned else 'unbanned'
        return jsonify({
            'success': True,
            'message': f'User {action}',
            'user': {
                'id': user.id,
                'email': user.email,
                'is_banned': user.is_banned
            }
        })

    finally:
        db.close()


@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(user_id):
    """
    Permanently delete a user and all their data.
    WARNING: This action cannot be undone.
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Prevent admin from deleting themselves
        current_user = get_current_user()
        if user.id == current_user.id:
            return jsonify({'error': 'Cannot delete your own account'}), 403

        # Prevent deleting other admins
        if user.is_admin:
            return jsonify({'error': 'Cannot delete admin users'}), 403

        # Delete user (cascade will delete related data)
        email = user.email
        db.delete(user)
        db.commit()

        return jsonify({
            'success': True,
            'message': f'User {email} permanently deleted'
        })

    finally:
        db.close()


# ============= CONTENT MODERATION =============

@admin_bp.route('/forum/posts', methods=['GET'])
@token_required
@admin_required
def get_all_forum_posts():
    """
    Get all forum posts including deleted ones for moderation.

    Query params:
    - category: Filter by category
    - deleted: Show only deleted (true) or only active (false), or all (not specified)
    - flagged: Show only flagged posts (not implemented yet)
    - limit: Results per page (default 50)
    - offset: Pagination offset (default 0)
    """
    db = SessionLocal()
    try:
        category = request.args.get('category')
        deleted_filter = request.args.get('deleted')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)

        # Build query (include deleted posts for moderation)
        query = db.query(ForumPost).filter(ForumPost.parent_id == None)

        if category:
            query = query.filter(ForumPost.category == category)

        if deleted_filter is not None:
            is_deleted = deleted_filter.lower() == 'true'
            query = query.filter(ForumPost.is_deleted == is_deleted)

        # Get total count
        total_count = query.count()

        # Order by created_at desc, paginate
        posts = query.order_by(desc(ForumPost.created_at)).limit(limit).offset(offset).all()

        # Format response
        posts_data = []
        for post in posts:
            # Get author info
            author = db.query(User).filter(User.id == post.user_id).first()

            # Count replies
            reply_count = db.query(ForumPost).filter(ForumPost.parent_id == post.id).count()

            posts_data.append({
                'id': post.id,
                'title': post.title,
                'content': post.content[:200] + '...' if len(post.content) > 200 else post.content,
                'category': post.category,
                'author': {
                    'id': author.id if author else None,
                    'email': author.email if author else 'Deleted User',
                    'name': author.name if author else 'Deleted User'
                },
                'created_at': post.created_at.isoformat() if post.created_at else None,
                'upvotes': post.upvotes,
                'downvotes': post.downvotes,
                'reply_count': reply_count,
                'is_pinned': post.is_pinned,
                'is_locked': post.is_locked,
                'is_deleted': post.is_deleted
            })

        return jsonify({
            'success': True,
            'posts': posts_data,
            'total': total_count,
            'limit': limit,
            'offset': offset
        })

    finally:
        db.close()


@admin_bp.route('/forum/posts/<int:post_id>/restore', methods=['POST'])
@token_required
@admin_required
def restore_forum_post(post_id):
    """Restore a deleted forum post."""
    db = SessionLocal()
    try:
        post = db.query(ForumPost).filter(ForumPost.id == post_id).first()

        if not post:
            return jsonify({'error': 'Post not found'}), 404

        if not post.is_deleted:
            return jsonify({'error': 'Post is not deleted'}), 400

        post.is_deleted = False
        db.commit()

        return jsonify({
            'success': True,
            'message': 'Post restored'
        })

    finally:
        db.close()


# ============= ANALYTICS =============

@admin_bp.route('/analytics/overview', methods=['GET'])
@token_required
@admin_required
def get_analytics_overview():
    """Get platform-wide analytics overview."""
    db = SessionLocal()
    try:
        # User statistics
        total_users = db.query(User).count()
        active_users_30d = db.query(User).filter(
            User.last_login >= datetime.utcnow() - timedelta(days=30)
        ).count()
        banned_users = db.query(User).filter(User.is_banned == True).count()

        # Subscription statistics
        free_users = db.query(User).filter(User.subscription_tier == 'free').count()
        pro_users = db.query(User).filter(User.subscription_tier == 'pro').count()
        enterprise_users = db.query(User).filter(User.subscription_tier == 'enterprise').count()

        # Course statistics
        total_enrollments = db.query(CourseProgress).count()
        completed_courses = db.query(CourseProgress).filter(
            CourseProgress.completed == True
        ).count()

        # Forum statistics
        total_posts = db.query(ForumPost).count()
        active_posts = db.query(ForumPost).filter(
            ForumPost.is_deleted == False
        ).count()
        deleted_posts = db.query(ForumPost).filter(
            ForumPost.is_deleted == True
        ).count()

        # Revenue statistics
        total_revenue = db.query(func.sum(Payment.amount)).filter(
            Payment.status == 'succeeded'
        ).scalar() or 0

        revenue_30d = db.query(func.sum(Payment.amount)).filter(
            and_(
                Payment.status == 'succeeded',
                Payment.created_at >= datetime.utcnow() - timedelta(days=30)
            )
        ).scalar() or 0

        return jsonify({
            'success': True,
            'analytics': {
                'users': {
                    'total': total_users,
                    'active_30d': active_users_30d,
                    'banned': banned_users,
                    'free': free_users,
                    'pro': pro_users,
                    'enterprise': enterprise_users
                },
                'courses': {
                    'total_enrollments': total_enrollments,
                    'completed': completed_courses,
                    'completion_rate': (completed_courses / total_enrollments * 100) if total_enrollments > 0 else 0
                },
                'forum': {
                    'total_posts': total_posts,
                    'active_posts': active_posts,
                    'deleted_posts': deleted_posts
                },
                'revenue': {
                    'total': total_revenue / 100,  # Convert cents to dollars
                    'last_30_days': revenue_30d / 100,
                    'mrr_estimate': (pro_users * 19) + (enterprise_users * 99)  # Monthly Recurring Revenue estimate
                }
            }
        })

    finally:
        db.close()


@admin_bp.route('/analytics/growth', methods=['GET'])
@token_required
@admin_required
def get_growth_analytics():
    """
    Get user growth analytics.

    Query params:
    - period: Time period (7d, 30d, 90d, 1y) default 30d
    """
    period = request.args.get('period', '30d')

    # Map period to days
    period_days = {
        '7d': 7,
        '30d': 30,
        '90d': 90,
        '1y': 365
    }

    days = period_days.get(period, 30)
    start_date = datetime.utcnow() - timedelta(days=days)

    db = SessionLocal()
    try:
        # New users in period
        new_users = db.query(User).filter(
            User.created_at >= start_date
        ).count()

        # New subscriptions in period
        new_pro = db.query(User).filter(
            and_(
                User.created_at >= start_date,
                User.subscription_tier == 'pro'
            )
        ).count()

        new_enterprise = db.query(User).filter(
            and_(
                User.created_at >= start_date,
                User.subscription_tier == 'enterprise'
            )
        ).count()

        # Revenue in period
        revenue = db.query(func.sum(Payment.amount)).filter(
            and_(
                Payment.status == 'succeeded',
                Payment.created_at >= start_date
            )
        ).scalar() or 0

        return jsonify({
            'success': True,
            'period': period,
            'growth': {
                'new_users': new_users,
                'new_pro_subscriptions': new_pro,
                'new_enterprise_subscriptions': new_enterprise,
                'revenue': revenue / 100,
                'average_revenue_per_user': (revenue / new_users / 100) if new_users > 0 else 0
            }
        })

    finally:
        db.close()


@admin_bp.route('/analytics/courses', methods=['GET'])
@token_required
@admin_required
def get_course_analytics():
    """Get course enrollment and completion analytics."""
    db = SessionLocal()
    try:
        # Get course statistics
        course_stats = db.query(
            CourseProgress.course_id,
            func.count(CourseProgress.id).label('enrollments'),
            func.sum(func.cast(CourseProgress.completed, db.Integer)).label('completions')
        ).group_by(CourseProgress.course_id).all()

        courses_data = []
        for course_id, enrollments, completions in course_stats:
            completion_rate = (completions / enrollments * 100) if enrollments > 0 else 0
            courses_data.append({
                'course_id': course_id,
                'enrollments': enrollments,
                'completions': completions or 0,
                'completion_rate': round(completion_rate, 2)
            })

        return jsonify({
            'success': True,
            'courses': courses_data
        })

    finally:
        db.close()


# ============= SYSTEM HEALTH =============

@admin_bp.route('/system/health', methods=['GET'])
@token_required
@admin_required
def get_system_health():
    """Get system health metrics."""
    db = SessionLocal()
    try:
        # Database connection test
        db.execute('SELECT 1')
        db_healthy = True

        # Get database stats
        total_records = {
            'users': db.query(User).count(),
            'forum_posts': db.query(ForumPost).count(),
            'course_progress': db.query(CourseProgress).count(),
            'payments': db.query(Payment).count()
        }

        return jsonify({
            'success': True,
            'health': {
                'database': 'healthy' if db_healthy else 'unhealthy',
                'api': 'healthy',  # If this endpoint responds, API is healthy
                'timestamp': datetime.utcnow().isoformat()
            },
            'database_stats': total_records
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'health': {
                'database': 'unhealthy',
                'api': 'degraded',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
        }), 503

    finally:
        db.close()


# ============= Main (for testing) =============

if __name__ == "__main__":
    print("=" * 60)
    print("ADMIN DASHBOARD API - Consciousness Platform")
    print("=" * 60)
    print("All endpoints require admin authentication (@admin_required)")
    print("\nUser Management:")
    print("  GET    /api/admin/users - List all users (filterable, paginated)")
    print("  GET    /api/admin/users/<id> - Get user details with statistics")
    print("  PUT    /api/admin/users/<id>/role - Update user role (promote/demote)")
    print("  PUT    /api/admin/users/<id>/ban - Ban or unban user")
    print("  DELETE /api/admin/users/<id> - Permanently delete user")
    print("\nContent Moderation:")
    print("  GET    /api/admin/forum/posts - Get all forum posts (including deleted)")
    print("  POST   /api/admin/forum/posts/<id>/restore - Restore deleted post")
    print("\nAnalytics:")
    print("  GET    /api/admin/analytics/overview - Platform-wide analytics")
    print("  GET    /api/admin/analytics/growth - User growth analytics")
    print("  GET    /api/admin/analytics/courses - Course enrollment/completion stats")
    print("\nSystem Health:")
    print("  GET    /api/admin/system/health - System health check")
    print("=" * 60)
