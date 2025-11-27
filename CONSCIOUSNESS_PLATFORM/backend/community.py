"""
COMMUNITY FORUM - Discussion and Engagement System
===================================================
API endpoints for community discussions, posts, and replies.

Work Order: Build 7 - Community Forum
Created: 2025-11-27
"""

import os
from datetime import datetime
from flask import Blueprint, request, jsonify
from sqlalchemy import and_, or_, desc
from auth import token_required, admin_required, get_current_user
from models import User, ForumPost, SessionLocal

# Create blueprint
community_bp = Blueprint('community', __name__, url_prefix='/api/community')


# ============= Forum Categories =============

FORUM_CATEGORIES = {
    'general': {
        'name': 'General Discussion',
        'description': 'General conversations about consciousness and pattern theory',
        'icon': '💬'
    },
    'success-stories': {
        'name': 'Success Stories',
        'description': 'Share your pattern recognition wins and consciousness breakthroughs',
        'icon': '🎉'
    },
    'questions': {
        'name': 'Questions & Help',
        'description': 'Ask questions and get help from the community',
        'icon': '❓'
    },
    'pattern-analysis': {
        'name': 'Pattern Analysis',
        'description': 'Analyze and discuss real-world patterns you\'ve observed',
        'icon': '🔍'
    },
    'resources': {
        'name': 'Resources & Tools',
        'description': 'Share useful resources, tools, and techniques',
        'icon': '📚'
    },
    'feedback': {
        'name': 'Platform Feedback',
        'description': 'Suggest improvements and report issues',
        'icon': '💡'
    }
}


@community_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    Get all forum categories.

    Response:
    {
        "success": true,
        "categories": [
            {
                "id": "general",
                "name": "General Discussion",
                "description": "...",
                "icon": "💬",
                "post_count": 42
            }
        ]
    }
    """
    try:
        db = SessionLocal()
        try:
            # Count posts per category
            categories = []
            for cat_id, cat_data in FORUM_CATEGORIES.items():
                post_count = db.query(ForumPost).filter(
                    and_(
                        ForumPost.category == cat_id,
                        ForumPost.parent_id == None,  # Only top-level posts
                        ForumPost.is_deleted == False
                    )
                ).count()

                categories.append({
                    'id': cat_id,
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'icon': cat_data['icon'],
                    'post_count': post_count
                })

            return jsonify({
                'success': True,
                'categories': categories
            })

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= Post Management =============

@community_bp.route('/posts', methods=['GET'])
def get_posts():
    """
    Get forum posts (with filtering and pagination).

    Query params:
        category: Filter by category
        sort: 'recent', 'popular', 'trending' (default: recent)
        limit: Posts per page (default: 20, max: 100)
        offset: Skip first N posts (default: 0)

    Response:
    {
        "success": true,
        "posts": [
            {
                "id": 1,
                "title": "How to detect manipulation in meetings",
                "content": "...",
                "category": "pattern-analysis",
                "author": {
                    "id": 5,
                    "username": "pattern_master",
                    "avatar_url": "..."
                },
                "upvotes": 42,
                "downvotes": 3,
                "reply_count": 15,
                "view_count": 234,
                "is_pinned": false,
                "is_locked": false,
                "created_at": "2025-11-27T10:00:00",
                "updated_at": "2025-11-27T12:30:00"
            }
        ],
        "total": 156,
        "has_more": true
    }
    """
    try:
        category = request.args.get('category')
        sort = request.args.get('sort', 'recent')
        limit = min(int(request.args.get('limit', 20)), 100)
        offset = int(request.args.get('offset', 0))

        db = SessionLocal()
        try:
            # Build query
            query = db.query(ForumPost).filter(
                and_(
                    ForumPost.parent_id == None,  # Only top-level posts
                    ForumPost.is_deleted == False
                )
            )

            # Filter by category
            if category:
                query = query.filter(ForumPost.category == category)

            # Sorting
            if sort == 'popular':
                query = query.order_by(desc(ForumPost.upvotes - ForumPost.downvotes))
            elif sort == 'trending':
                # Trending = high engagement recently (simplified: upvotes + view_count)
                query = query.order_by(desc(ForumPost.upvotes + ForumPost.view_count))
            else:  # recent
                # Pinned posts first, then by creation date
                query = query.order_by(desc(ForumPost.is_pinned), desc(ForumPost.created_at))

            # Get total count
            total = query.count()

            # Apply pagination
            posts_data = query.limit(limit).offset(offset).all()

            # Build response
            posts = []
            for post in posts_data:
                # Get reply count
                reply_count = db.query(ForumPost).filter(
                    and_(
                        ForumPost.parent_id == post.id,
                        ForumPost.is_deleted == False
                    )
                ).count()

                # Get author info
                author = db.query(User).filter(User.id == post.user_id).first()

                posts.append({
                    'id': post.id,
                    'title': post.title,
                    'content': post.content[:500] + ('...' if len(post.content) > 500 else ''),  # Preview
                    'category': post.category,
                    'author': {
                        'id': author.id,
                        'username': author.username or author.email.split('@')[0],
                        'avatar_url': author.avatar_url
                    } if author else None,
                    'upvotes': post.upvotes,
                    'downvotes': post.downvotes,
                    'reply_count': reply_count,
                    'view_count': post.view_count,
                    'is_pinned': post.is_pinned,
                    'is_locked': post.is_locked,
                    'created_at': post.created_at.isoformat() if post.created_at else None,
                    'updated_at': post.updated_at.isoformat() if post.updated_at else None
                })

            return jsonify({
                'success': True,
                'posts': posts,
                'total': total,
                'has_more': (offset + limit) < total
            })

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@community_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """
    Get single post with all replies.

    Response:
    {
        "success": true,
        "post": {
            "id": 1,
            "title": "...",
            "content": "...",
            "category": "...",
            "author": {...},
            "upvotes": 42,
            "downvotes": 3,
            "view_count": 234,
            "is_pinned": false,
            "is_locked": false,
            "created_at": "...",
            "updated_at": "...",
            "replies": [
                {
                    "id": 2,
                    "content": "...",
                    "author": {...},
                    "upvotes": 5,
                    "downvotes": 0,
                    "created_at": "..."
                }
            ]
        }
    }
    """
    try:
        db = SessionLocal()
        try:
            # Get post
            post = db.query(ForumPost).filter(
                and_(
                    ForumPost.id == post_id,
                    ForumPost.is_deleted == False
                )
            ).first()

            if not post:
                return jsonify({'error': 'Post not found'}), 404

            # Increment view count
            post.view_count += 1
            db.commit()

            # Get author
            author = db.query(User).filter(User.id == post.user_id).first()

            # Get replies
            replies_data = db.query(ForumPost).filter(
                and_(
                    ForumPost.parent_id == post_id,
                    ForumPost.is_deleted == False
                )
            ).order_by(ForumPost.created_at).all()

            replies = []
            for reply in replies_data:
                reply_author = db.query(User).filter(User.id == reply.user_id).first()
                replies.append({
                    'id': reply.id,
                    'content': reply.content,
                    'author': {
                        'id': reply_author.id,
                        'username': reply_author.username or reply_author.email.split('@')[0],
                        'avatar_url': reply_author.avatar_url
                    } if reply_author else None,
                    'upvotes': reply.upvotes,
                    'downvotes': reply.downvotes,
                    'created_at': reply.created_at.isoformat() if reply.created_at else None,
                    'updated_at': reply.updated_at.isoformat() if reply.updated_at else None
                })

            return jsonify({
                'success': True,
                'post': {
                    'id': post.id,
                    'title': post.title,
                    'content': post.content,
                    'category': post.category,
                    'author': {
                        'id': author.id,
                        'username': author.username or author.email.split('@')[0],
                        'avatar_url': author.avatar_url
                    } if author else None,
                    'upvotes': post.upvotes,
                    'downvotes': post.downvotes,
                    'view_count': post.view_count,
                    'is_pinned': post.is_pinned,
                    'is_locked': post.is_locked,
                    'created_at': post.created_at.isoformat() if post.created_at else None,
                    'updated_at': post.updated_at.isoformat() if post.updated_at else None,
                    'replies': replies
                }
            })

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@community_bp.route('/posts', methods=['POST'])
@token_required
def create_post():
    """
    Create new forum post.

    Headers:
        Authorization: Bearer <access_token>

    Request body:
    {
        "title": "How to detect manipulation in meetings",
        "content": "I've been practicing...",
        "category": "pattern-analysis"
    }

    Response:
    {
        "success": true,
        "post": {
            "id": 1,
            "title": "...",
            ...
        }
    }
    """
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Pro subscription required to post
        if user.subscription_tier not in ['pro', 'enterprise']:
            return jsonify({
                'error': 'Pro subscription required to create posts'
            }), 403

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing request body'}), 400

        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        category = data.get('category', 'general')

        # Validation
        if not title or len(title) < 5:
            return jsonify({'error': 'Title must be at least 5 characters'}), 400

        if not content or len(content) < 20:
            return jsonify({'error': 'Content must be at least 20 characters'}), 400

        if category not in FORUM_CATEGORIES:
            return jsonify({'error': 'Invalid category'}), 400

        db = SessionLocal()
        try:
            # Create post
            post = ForumPost(
                user_id=user.id,
                title=title,
                content=content,
                category=category,
                upvotes=0,
                downvotes=0,
                view_count=0,
                is_pinned=False,
                is_locked=False,
                is_deleted=False,
                created_at=datetime.utcnow()
            )

            db.add(post)
            db.commit()
            db.refresh(post)

            return jsonify({
                'success': True,
                'post': {
                    'id': post.id,
                    'title': post.title,
                    'content': post.content,
                    'category': post.category,
                    'created_at': post.created_at.isoformat()
                }
            }), 201

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@community_bp.route('/posts/<int:post_id>/reply', methods=['POST'])
@token_required
def reply_to_post(post_id):
    """
    Reply to a forum post.

    Headers:
        Authorization: Bearer <access_token>

    Request body:
    {
        "content": "Great observation! I've noticed..."
    }

    Response:
    {
        "success": true,
        "reply": {
            "id": 2,
            "content": "...",
            "created_at": "..."
        }
    }
    """
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Pro subscription required to reply
        if user.subscription_tier not in ['pro', 'enterprise']:
            return jsonify({
                'error': 'Pro subscription required to reply to posts'
            }), 403

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing request body'}), 400

        content = data.get('content', '').strip()

        if not content or len(content) < 10:
            return jsonify({'error': 'Reply must be at least 10 characters'}), 400

        db = SessionLocal()
        try:
            # Check parent post exists and is not locked/deleted
            parent_post = db.query(ForumPost).filter(
                and_(
                    ForumPost.id == post_id,
                    ForumPost.is_deleted == False
                )
            ).first()

            if not parent_post:
                return jsonify({'error': 'Post not found'}), 404

            if parent_post.is_locked:
                return jsonify({'error': 'Post is locked'}), 403

            # Create reply
            reply = ForumPost(
                user_id=user.id,
                parent_id=post_id,
                title='',  # Replies don't have titles
                content=content,
                category=parent_post.category,  # Inherit category
                upvotes=0,
                downvotes=0,
                view_count=0,
                is_pinned=False,
                is_locked=False,
                is_deleted=False,
                created_at=datetime.utcnow()
            )

            db.add(reply)
            db.commit()
            db.refresh(reply)

            return jsonify({
                'success': True,
                'reply': {
                    'id': reply.id,
                    'content': reply.content,
                    'created_at': reply.created_at.isoformat()
                }
            }), 201

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@community_bp.route('/posts/<int:post_id>/vote', methods=['POST'])
@token_required
def vote_on_post(post_id):
    """
    Upvote or downvote a post.

    Headers:
        Authorization: Bearer <access_token>

    Request body:
    {
        "vote": "up" | "down"
    }

    Response:
    {
        "success": true,
        "upvotes": 43,
        "downvotes": 3
    }
    """
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing request body'}), 400

        vote = data.get('vote')
        if vote not in ['up', 'down']:
            return jsonify({'error': 'Vote must be "up" or "down"'}), 400

        db = SessionLocal()
        try:
            post = db.query(ForumPost).filter(
                and_(
                    ForumPost.id == post_id,
                    ForumPost.is_deleted == False
                )
            ).first()

            if not post:
                return jsonify({'error': 'Post not found'}), 404

            # Simple voting (no vote tracking per user for MVP)
            if vote == 'up':
                post.upvotes += 1
            else:
                post.downvotes += 1

            db.commit()

            return jsonify({
                'success': True,
                'upvotes': post.upvotes,
                'downvotes': post.downvotes
            })

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= Moderation =============

@community_bp.route('/posts/<int:post_id>/pin', methods=['POST'])
@token_required
@admin_required
def pin_post(post_id):
    """Pin/unpin a post (admin only)."""
    try:
        data = request.get_json() or {}
        pinned = data.get('pinned', True)

        db = SessionLocal()
        try:
            post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
            if not post:
                return jsonify({'error': 'Post not found'}), 404

            post.is_pinned = pinned
            db.commit()

            return jsonify({
                'success': True,
                'message': f'Post {"pinned" if pinned else "unpinned"}'
            })

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@community_bp.route('/posts/<int:post_id>/lock', methods=['POST'])
@token_required
@admin_required
def lock_post(post_id):
    """Lock/unlock a post (admin only)."""
    try:
        data = request.get_json() or {}
        locked = data.get('locked', True)

        db = SessionLocal()
        try:
            post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
            if not post:
                return jsonify({'error': 'Post not found'}), 404

            post.is_locked = locked
            db.commit()

            return jsonify({
                'success': True,
                'message': f'Post {"locked" if locked else "unlocked"}'
            })

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@community_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@token_required
def delete_post(post_id):
    """Delete a post (author or admin only)."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        db = SessionLocal()
        try:
            post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
            if not post:
                return jsonify({'error': 'Post not found'}), 404

            # Only author or admin can delete
            if post.user_id != user.id and not user.is_admin:
                return jsonify({'error': 'Unauthorized'}), 403

            # Soft delete
            post.is_deleted = True
            db.commit()

            return jsonify({
                'success': True,
                'message': 'Post deleted'
            })

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= User Activity =============

@community_bp.route('/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    """
    Get all posts by a specific user.

    Query params:
        limit: Posts per page (default: 20, max: 100)
        offset: Skip first N posts (default: 0)

    Response:
    {
        "success": true,
        "user": {
            "id": 5,
            "username": "pattern_master"
        },
        "posts": [...],
        "total": 23
    }
    """
    try:
        limit = min(int(request.args.get('limit', 20)), 100)
        offset = int(request.args.get('offset', 0))

        db = SessionLocal()
        try:
            # Get user
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return jsonify({'error': 'User not found'}), 404

            # Get posts
            query = db.query(ForumPost).filter(
                and_(
                    ForumPost.user_id == user_id,
                    ForumPost.parent_id == None,  # Only top-level posts
                    ForumPost.is_deleted == False
                )
            ).order_by(desc(ForumPost.created_at))

            total = query.count()
            posts_data = query.limit(limit).offset(offset).all()

            posts = []
            for post in posts_data:
                reply_count = db.query(ForumPost).filter(
                    and_(
                        ForumPost.parent_id == post.id,
                        ForumPost.is_deleted == False
                    )
                ).count()

                posts.append({
                    'id': post.id,
                    'title': post.title,
                    'category': post.category,
                    'upvotes': post.upvotes,
                    'downvotes': post.downvotes,
                    'reply_count': reply_count,
                    'view_count': post.view_count,
                    'created_at': post.created_at.isoformat() if post.created_at else None
                })

            return jsonify({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username or user.email.split('@')[0],
                    'avatar_url': user.avatar_url
                },
                'posts': posts,
                'total': total,
                'has_more': (offset + limit) < total
            })

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500
