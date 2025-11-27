"""
PATTERN THEORY ACADEMY - Course Delivery System
================================================
API endpoints for educational content delivery and progress tracking.

Work Order: Build 5 - Course System
Created: 2025-11-27
"""

import json
import os
from datetime import datetime
from flask import Blueprint, request, jsonify
from sqlalchemy import and_
from auth import token_required, subscription_required, get_current_user
from models import User, CourseProgress, SessionLocal
from email_service import (
    send_course_started_email,
    send_lesson_completed_email,
    send_course_completed_email
)

# Create blueprint
academy_bp = Blueprint('academy', __name__, url_prefix='/api/academy')

# Load course content
COURSE_CONTENT_PATH = os.path.join(os.path.dirname(__file__), 'course_content.json')

def load_course_content():
    """Load course content from JSON file"""
    try:
        with open(COURSE_CONTENT_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading course content: {e}")
        return {"courses": {}}

# Global course content (loaded once on startup)
COURSE_DATA = load_course_content()


# ============= Course Catalog =============

@academy_bp.route('/courses', methods=['GET'])
@token_required
def get_courses():
    """
    Get list of all available courses.

    Headers:
        Authorization: Bearer <access_token>

    Response:
    {
        "success": true,
        "courses": [
            {
                "id": "pattern-theory-foundations",
                "title": "Pattern Theory Foundations",
                "description": "...",
                "difficulty": "beginner",
                "duration_hours": 8,
                "tier_required": "pro",
                "lesson_count": 4,
                "user_progress": {
                    "started": true,
                    "completed_lessons": 2,
                    "total_lessons": 4,
                    "percent_complete": 50
                }
            }
        ]
    }
    """
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        db = SessionLocal()
        try:
            courses = []

            for course_id, course_data in COURSE_DATA.get('courses', {}).items():
                # Get user's progress for this course
                progress_records = db.query(CourseProgress).filter(
                    and_(
                        CourseProgress.user_id == user.id,
                        CourseProgress.course_id == course_id
                    )
                ).all()

                completed_lessons = sum(1 for p in progress_records if p.completed)
                total_lessons = len(course_data.get('lessons', []))

                user_progress = None
                if progress_records:
                    user_progress = {
                        'started': True,
                        'completed_lessons': completed_lessons,
                        'total_lessons': total_lessons,
                        'percent_complete': int((completed_lessons / total_lessons * 100)) if total_lessons > 0 else 0
                    }

                # Build course summary
                course_summary = {
                    'id': course_data.get('id'),
                    'title': course_data.get('title'),
                    'description': course_data.get('description'),
                    'difficulty': course_data.get('difficulty'),
                    'duration_hours': course_data.get('duration_hours'),
                    'tier_required': course_data.get('tier_required'),
                    'order': course_data.get('order'),
                    'lesson_count': total_lessons,
                    'user_progress': user_progress
                }

                courses.append(course_summary)

            # Sort by order
            courses.sort(key=lambda x: x.get('order', 999))

            return jsonify({
                'success': True,
                'courses': courses
            })

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@academy_bp.route('/courses/<course_id>', methods=['GET'])
@token_required
@subscription_required('pro')
def get_course(course_id):
    """
    Get detailed course information including all lessons.

    Headers:
        Authorization: Bearer <access_token>

    Params:
        course_id: Course identifier (e.g., 'pattern-theory-foundations')

    Response:
    {
        "success": true,
        "course": {
            "id": "...",
            "title": "...",
            "description": "...",
            "lessons": [
                {
                    "id": "intro-to-patterns",
                    "title": "Introduction to Pattern Theory",
                    "order": 1,
                    "duration_minutes": 30,
                    "completed": false
                }
            ],
            "user_progress": {
                "completed_lessons": 2,
                "total_lessons": 4,
                "percent_complete": 50,
                "current_lesson": "consciousness-levels"
            }
        }
    }
    """
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get course data
        course_data = COURSE_DATA.get('courses', {}).get(course_id)
        if not course_data:
            return jsonify({'error': 'Course not found'}), 404

        # Check tier requirement
        tier_required = course_data.get('tier_required', 'free')
        if not check_tier_access(user.subscription_tier, tier_required):
            return jsonify({
                'error': f'This course requires {tier_required} subscription or higher'
            }), 403

        db = SessionLocal()
        try:
            # Get user's progress for all lessons
            progress_records = db.query(CourseProgress).filter(
                and_(
                    CourseProgress.user_id == user.id,
                    CourseProgress.course_id == course_id
                )
            ).all()

            progress_map = {p.lesson_id: p for p in progress_records}

            # Build lesson summaries (without full content)
            lessons = []
            completed_count = 0
            current_lesson = None

            for lesson in course_data.get('lessons', []):
                lesson_id = lesson.get('id')
                progress = progress_map.get(lesson_id)

                is_completed = progress.completed if progress else False
                if is_completed:
                    completed_count += 1
                elif current_lesson is None:
                    current_lesson = lesson_id

                lesson_summary = {
                    'id': lesson_id,
                    'title': lesson.get('title'),
                    'order': lesson.get('order'),
                    'duration_minutes': lesson.get('duration_minutes'),
                    'completed': is_completed,
                    'started': progress is not None,
                    'progress_percent': progress.progress_percent if progress else 0
                }

                lessons.append(lesson_summary)

            total_lessons = len(lessons)
            percent_complete = int((completed_count / total_lessons * 100)) if total_lessons > 0 else 0

            return jsonify({
                'success': True,
                'course': {
                    'id': course_data.get('id'),
                    'title': course_data.get('title'),
                    'description': course_data.get('description'),
                    'difficulty': course_data.get('difficulty'),
                    'duration_hours': course_data.get('duration_hours'),
                    'tier_required': tier_required,
                    'lessons': lessons,
                    'user_progress': {
                        'completed_lessons': completed_count,
                        'total_lessons': total_lessons,
                        'percent_complete': percent_complete,
                        'current_lesson': current_lesson
                    }
                }
            })

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= Lesson Content =============

@academy_bp.route('/courses/<course_id>/lessons/<lesson_id>', methods=['GET'])
@token_required
@subscription_required('pro')
def get_lesson(course_id, lesson_id):
    """
    Get full lesson content.

    Headers:
        Authorization: Bearer <access_token>

    Params:
        course_id: Course identifier
        lesson_id: Lesson identifier

    Response:
    {
        "success": true,
        "lesson": {
            "id": "intro-to-patterns",
            "title": "Introduction to Pattern Theory",
            "order": 1,
            "duration_minutes": 30,
            "content": {...},
            "quiz": {...},
            "completed": false,
            "progress_percent": 0
        },
        "navigation": {
            "previous_lesson": null,
            "next_lesson": "seven-domains-overview"
        }
    }
    """
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get course data
        course_data = COURSE_DATA.get('courses', {}).get(course_id)
        if not course_data:
            return jsonify({'error': 'Course not found'}), 404

        # Check tier requirement
        tier_required = course_data.get('tier_required', 'free')
        if not check_tier_access(user.subscription_tier, tier_required):
            return jsonify({
                'error': f'This course requires {tier_required} subscription or higher'
            }), 403

        # Find lesson
        lessons = course_data.get('lessons', [])
        lesson_data = None
        lesson_index = -1

        for idx, lesson in enumerate(lessons):
            if lesson.get('id') == lesson_id:
                lesson_data = lesson
                lesson_index = idx
                break

        if not lesson_data:
            return jsonify({'error': 'Lesson not found'}), 404

        db = SessionLocal()
        try:
            # Get or create progress record
            progress = db.query(CourseProgress).filter(
                and_(
                    CourseProgress.user_id == user.id,
                    CourseProgress.course_id == course_id,
                    CourseProgress.lesson_id == lesson_id
                )
            ).first()

            if not progress:
                # Create new progress record
                progress = CourseProgress(
                    user_id=user.id,
                    course_id=course_id,
                    lesson_id=lesson_id,
                    completed=False,
                    progress_percent=0,
                    started_at=datetime.utcnow()
                )
                db.add(progress)
                db.commit()

                # Check if this is the first lesson in this course
                all_course_progress = db.query(CourseProgress).filter(
                    and_(
                        CourseProgress.user_id == user.id,
                        CourseProgress.course_id == course_id
                    )
                ).count()

                # If this is the first lesson, send course started email
                if all_course_progress == 1:  # Only this newly created progress record
                    lesson_count = len(course_data.get('lessons', []))
                    send_course_started_email(
                        user.email,
                        user.full_name,
                        course_data.get('title'),
                        lesson_count
                    )
            else:
                # Update last accessed
                progress.last_accessed = datetime.utcnow()
                db.commit()

            # Build navigation
            navigation = {
                'previous_lesson': lessons[lesson_index - 1].get('id') if lesson_index > 0 else None,
                'next_lesson': lessons[lesson_index + 1].get('id') if lesson_index < len(lessons) - 1 else None
            }

            return jsonify({
                'success': True,
                'lesson': {
                    'id': lesson_data.get('id'),
                    'title': lesson_data.get('title'),
                    'order': lesson_data.get('order'),
                    'duration_minutes': lesson_data.get('duration_minutes'),
                    'content': lesson_data.get('content'),
                    'quiz': lesson_data.get('quiz'),
                    'completed': progress.completed,
                    'progress_percent': progress.progress_percent,
                    'started_at': progress.started_at.isoformat() if progress.started_at else None
                },
                'navigation': navigation
            })

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= Quiz Submission =============

@academy_bp.route('/courses/<course_id>/lessons/<lesson_id>/quiz', methods=['POST'])
@token_required
@subscription_required('pro')
def submit_quiz(course_id, lesson_id):
    """
    Submit quiz answers and get results.

    Headers:
        Authorization: Bearer <access_token>

    Request body:
    {
        "answers": {
            "q1": 1,
            "q2": 0,
            "q3": 2
        }
    }

    Response:
    {
        "success": true,
        "results": {
            "score": 0.85,
            "passing_score": 0.7,
            "passed": true,
            "correct_answers": 3,
            "total_questions": 4,
            "question_results": [
                {
                    "question_id": "q1",
                    "correct": true,
                    "explanation": "..."
                }
            ]
        },
        "lesson_completed": true
    }
    """
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing request body'}), 400

        answers = data.get('answers', {})

        # Get course and lesson data
        course_data = COURSE_DATA.get('courses', {}).get(course_id)
        if not course_data:
            return jsonify({'error': 'Course not found'}), 404

        lesson_data = None
        for lesson in course_data.get('lessons', []):
            if lesson.get('id') == lesson_id:
                lesson_data = lesson
                break

        if not lesson_data:
            return jsonify({'error': 'Lesson not found'}), 404

        quiz_data = lesson_data.get('quiz')
        if not quiz_data:
            return jsonify({'error': 'This lesson has no quiz'}), 400

        # Grade quiz
        questions = quiz_data.get('questions', [])
        correct_count = 0
        question_results = []

        for question in questions:
            question_id = question.get('id')
            user_answer = answers.get(question_id)
            correct_answer = question.get('correct')

            is_correct = user_answer == correct_answer
            if is_correct:
                correct_count += 1

            question_results.append({
                'question_id': question_id,
                'correct': is_correct,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'explanation': question.get('explanation')
            })

        total_questions = len(questions)
        score = correct_count / total_questions if total_questions > 0 else 0
        passing_score = quiz_data.get('passing_score', 0.7)
        passed = score >= passing_score

        # Update progress
        db = SessionLocal()
        try:
            progress = db.query(CourseProgress).filter(
                and_(
                    CourseProgress.user_id == user.id,
                    CourseProgress.course_id == course_id,
                    CourseProgress.lesson_id == lesson_id
                )
            ).first()

            if not progress:
                progress = CourseProgress(
                    user_id=user.id,
                    course_id=course_id,
                    lesson_id=lesson_id,
                    started_at=datetime.utcnow()
                )
                db.add(progress)

            # Update quiz data
            if not progress.lesson_data:
                progress.lesson_data = {}

            if 'quiz_attempts' not in progress.lesson_data:
                progress.lesson_data['quiz_attempts'] = []

            progress.lesson_data['quiz_attempts'].append({
                'timestamp': datetime.utcnow().isoformat(),
                'score': score,
                'passed': passed
            })

            progress.lesson_data['best_score'] = max(
                score,
                progress.lesson_data.get('best_score', 0)
            )

            # Mark lesson complete if quiz passed
            lesson_just_completed = False
            if passed and not progress.completed:
                progress.completed = True
                progress.completed_at = datetime.utcnow()
                progress.progress_percent = 100
                lesson_just_completed = True

            db.commit()

            # Send lesson completion email if just completed
            if lesson_just_completed:
                send_lesson_completed_email(
                    user.email,
                    user.full_name,
                    course_data.get('title'),
                    lesson_data.get('title'),
                    score
                )

                # Check if all lessons in course are now completed
                all_course_progress = db.query(CourseProgress).filter(
                    and_(
                        CourseProgress.user_id == user.id,
                        CourseProgress.course_id == course_id
                    )
                ).all()

                total_lessons = len(course_data.get('lessons', []))
                completed_lessons = sum(1 for p in all_course_progress if p.completed)

                # If all lessons completed, send course completion email
                if completed_lessons == total_lessons:
                    # Find next course in sequence
                    next_course_title = None
                    current_order = course_data.get('order', 999)
                    for cid, cdata in COURSE_DATA.get('courses', {}).items():
                        if cdata.get('order', 999) == current_order + 1:
                            next_course_title = cdata.get('title')
                            break

                    send_course_completed_email(
                        user.email,
                        user.full_name,
                        course_data.get('title'),
                        total_lessons,
                        next_course_title
                    )

            return jsonify({
                'success': True,
                'results': {
                    'score': round(score, 2),
                    'passing_score': passing_score,
                    'passed': passed,
                    'correct_answers': correct_count,
                    'total_questions': total_questions,
                    'question_results': question_results
                },
                'lesson_completed': progress.completed
            })

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= Progress Tracking =============

@academy_bp.route('/courses/<course_id>/lessons/<lesson_id>/complete', methods=['POST'])
@token_required
@subscription_required('pro')
def complete_lesson(course_id, lesson_id):
    """
    Mark lesson as complete (for lessons without quizzes).

    Headers:
        Authorization: Bearer <access_token>

    Response:
    {
        "success": true,
        "message": "Lesson marked complete",
        "course_progress": {
            "completed_lessons": 3,
            "total_lessons": 4,
            "percent_complete": 75
        }
    }
    """
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Verify course and lesson exist
        course_data = COURSE_DATA.get('courses', {}).get(course_id)
        if not course_data:
            return jsonify({'error': 'Course not found'}), 404

        lesson_exists = any(
            lesson.get('id') == lesson_id
            for lesson in course_data.get('lessons', [])
        )

        if not lesson_exists:
            return jsonify({'error': 'Lesson not found'}), 404

        db = SessionLocal()
        try:
            # Get or create progress
            progress = db.query(CourseProgress).filter(
                and_(
                    CourseProgress.user_id == user.id,
                    CourseProgress.course_id == course_id,
                    CourseProgress.lesson_id == lesson_id
                )
            ).first()

            if not progress:
                progress = CourseProgress(
                    user_id=user.id,
                    course_id=course_id,
                    lesson_id=lesson_id,
                    started_at=datetime.utcnow()
                )
                db.add(progress)

            # Mark complete
            if not progress.completed:
                progress.completed = True
                progress.completed_at = datetime.utcnow()
                progress.progress_percent = 100
                db.commit()

            # Calculate overall course progress
            all_progress = db.query(CourseProgress).filter(
                and_(
                    CourseProgress.user_id == user.id,
                    CourseProgress.course_id == course_id
                )
            ).all()

            completed_count = sum(1 for p in all_progress if p.completed)
            total_lessons = len(course_data.get('lessons', []))
            percent_complete = int((completed_count / total_lessons * 100)) if total_lessons > 0 else 0

            return jsonify({
                'success': True,
                'message': 'Lesson marked complete',
                'course_progress': {
                    'completed_lessons': completed_count,
                    'total_lessons': total_lessons,
                    'percent_complete': percent_complete
                }
            })

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@academy_bp.route('/progress', methods=['GET'])
@token_required
def get_overall_progress():
    """
    Get user's overall academy progress across all courses.

    Headers:
        Authorization: Bearer <access_token>

    Response:
    {
        "success": true,
        "progress": {
            "courses_started": 2,
            "courses_completed": 1,
            "total_lessons_completed": 8,
            "total_time_minutes": 240,
            "courses": [
                {
                    "course_id": "pattern-theory-foundations",
                    "title": "Pattern Theory Foundations",
                    "completed_lessons": 4,
                    "total_lessons": 4,
                    "percent_complete": 100,
                    "completed": true,
                    "started_at": "2025-11-27T10:00:00",
                    "completed_at": "2025-11-27T14:30:00"
                }
            ]
        }
    }
    """
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        db = SessionLocal()
        try:
            # Get all user progress
            all_progress = db.query(CourseProgress).filter(
                CourseProgress.user_id == user.id
            ).all()

            # Group by course
            course_progress_map = {}
            for progress in all_progress:
                course_id = progress.course_id
                if course_id not in course_progress_map:
                    course_progress_map[course_id] = []
                course_progress_map[course_id].append(progress)

            # Build course summaries
            courses = []
            courses_started = 0
            courses_completed = 0
            total_lessons_completed = 0

            for course_id, progress_list in course_progress_map.items():
                course_data = COURSE_DATA.get('courses', {}).get(course_id)
                if not course_data:
                    continue

                completed_lessons = sum(1 for p in progress_list if p.completed)
                total_lessons = len(course_data.get('lessons', []))
                percent_complete = int((completed_lessons / total_lessons * 100)) if total_lessons > 0 else 0

                is_completed = completed_lessons == total_lessons

                # Get timestamps
                started_at = min(p.started_at for p in progress_list if p.started_at)
                completed_at = None
                if is_completed:
                    completed_times = [p.completed_at for p in progress_list if p.completed_at]
                    if completed_times:
                        completed_at = max(completed_times)

                courses.append({
                    'course_id': course_id,
                    'title': course_data.get('title'),
                    'completed_lessons': completed_lessons,
                    'total_lessons': total_lessons,
                    'percent_complete': percent_complete,
                    'completed': is_completed,
                    'started_at': started_at.isoformat() if started_at else None,
                    'completed_at': completed_at.isoformat() if completed_at else None
                })

                courses_started += 1
                if is_completed:
                    courses_completed += 1
                total_lessons_completed += completed_lessons

            # Sort by most recent
            courses.sort(key=lambda x: x.get('started_at', ''), reverse=True)

            return jsonify({
                'success': True,
                'progress': {
                    'courses_started': courses_started,
                    'courses_completed': courses_completed,
                    'total_lessons_completed': total_lessons_completed,
                    'courses': courses
                }
            })

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@academy_bp.route('/progress/<course_id>', methods=['GET'])
@token_required
def get_course_progress(course_id):
    """
    Get detailed progress for specific course.

    Headers:
        Authorization: Bearer <access_token>

    Response:
    {
        "success": true,
        "progress": {
            "course_id": "pattern-theory-foundations",
            "title": "Pattern Theory Foundations",
            "completed_lessons": 2,
            "total_lessons": 4,
            "percent_complete": 50,
            "started_at": "2025-11-27T10:00:00",
            "lessons": [
                {
                    "lesson_id": "intro-to-patterns",
                    "title": "Introduction to Pattern Theory",
                    "completed": true,
                    "started_at": "2025-11-27T10:00:00",
                    "completed_at": "2025-11-27T10:35:00",
                    "quiz_score": 0.85
                }
            ]
        }
    }
    """
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get course data
        course_data = COURSE_DATA.get('courses', {}).get(course_id)
        if not course_data:
            return jsonify({'error': 'Course not found'}), 404

        db = SessionLocal()
        try:
            # Get progress for this course
            progress_records = db.query(CourseProgress).filter(
                and_(
                    CourseProgress.user_id == user.id,
                    CourseProgress.course_id == course_id
                )
            ).all()

            if not progress_records:
                return jsonify({
                    'success': True,
                    'progress': {
                        'course_id': course_id,
                        'title': course_data.get('title'),
                        'completed_lessons': 0,
                        'total_lessons': len(course_data.get('lessons', [])),
                        'percent_complete': 0,
                        'started_at': None,
                        'lessons': []
                    }
                })

            # Build lesson progress list
            progress_map = {p.lesson_id: p for p in progress_records}
            lessons_progress = []

            for lesson in course_data.get('lessons', []):
                lesson_id = lesson.get('id')
                progress = progress_map.get(lesson_id)

                if progress:
                    quiz_score = None
                    if progress.lesson_data and 'best_score' in progress.lesson_data:
                        quiz_score = progress.lesson_data['best_score']

                    lessons_progress.append({
                        'lesson_id': lesson_id,
                        'title': lesson.get('title'),
                        'completed': progress.completed,
                        'started_at': progress.started_at.isoformat() if progress.started_at else None,
                        'completed_at': progress.completed_at.isoformat() if progress.completed_at else None,
                        'quiz_score': quiz_score
                    })

            completed_count = sum(1 for p in progress_records if p.completed)
            total_lessons = len(course_data.get('lessons', []))
            percent_complete = int((completed_count / total_lessons * 100)) if total_lessons > 0 else 0
            started_at = min(p.started_at for p in progress_records if p.started_at)

            return jsonify({
                'success': True,
                'progress': {
                    'course_id': course_id,
                    'title': course_data.get('title'),
                    'completed_lessons': completed_count,
                    'total_lessons': total_lessons,
                    'percent_complete': percent_complete,
                    'started_at': started_at.isoformat() if started_at else None,
                    'lessons': lessons_progress
                }
            })

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= Utilities =============

def check_tier_access(user_tier, required_tier):
    """Check if user's tier grants access to required tier"""
    tier_hierarchy = ['free', 'pro', 'enterprise']

    try:
        user_level = tier_hierarchy.index(user_tier)
        required_level = tier_hierarchy.index(required_tier)
        return user_level >= required_level
    except ValueError:
        return False
