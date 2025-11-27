"""
EMAIL SERVICE - Consciousness Platform
========================================
SendGrid email integration for transactional emails.

Created: 2025-11-27
"""

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from typing import List, Optional, Dict, Any
from datetime import datetime

# SendGrid configuration
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = os.environ.get("SENDGRID_FROM_EMAIL", "noreply@consciousnessplatform.com")
SENDGRID_FROM_NAME = os.environ.get("SENDGRID_FROM_NAME", "Consciousness Platform")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")

# Initialize SendGrid client
sg = SendGridAPIClient(SENDGRID_API_KEY) if SENDGRID_API_KEY else None


# ============= Core Email Function =============

def send_email(to_email: str, subject: str, html_content: str,
               text_content: Optional[str] = None) -> tuple[bool, Optional[str]]:
    """
    Send email via SendGrid.

    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML email body
        text_content: Plain text email body (optional)

    Returns:
        (success, error_message)
    """
    if not sg:
        print("SendGrid not configured - email not sent")
        return False, "SendGrid API key not configured"

    try:
        message = Mail(
            from_email=Email(SENDGRID_FROM_EMAIL, SENDGRID_FROM_NAME),
            to_emails=To(to_email),
            subject=subject,
            html_content=Content("text/html", html_content)
        )

        if text_content:
            message.add_content(Content("text/plain", text_content))

        response = sg.send(message)

        if response.status_code in [200, 201, 202]:
            print(f"Email sent successfully to {to_email}: {subject}")
            return True, None
        else:
            error = f"SendGrid error: {response.status_code}"
            print(error)
            return False, error

    except Exception as e:
        error = f"Failed to send email: {str(e)}"
        print(error)
        return False, error


# ============= Welcome Email =============

def send_welcome_email(user_email: str, user_name: Optional[str] = None) -> tuple[bool, Optional[str]]:
    """Send welcome email to new user"""

    display_name = user_name or user_email.split('@')[0]

    subject = "Welcome to Consciousness Platform 🌟"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; }}
            .button {{ background: #667eea; color: white; padding: 12px 30px;
                      text-decoration: none; border-radius: 5px; display: inline-block;
                      margin: 20px 0; }}
            .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to Consciousness Platform!</h1>
            </div>
            <div class="content">
                <p>Hi {display_name},</p>

                <p>Welcome to your journey of consciousness elevation! We're excited to have you join our community.</p>

                <h3>What's Next?</h3>
                <ul>
                    <li><strong>Take the Consciousness Bridge Assessment</strong> - Discover your consciousness level in 3 minutes</li>
                    <li><strong>Explore Pattern Theory</strong> - Learn to detect manipulation in real-time</li>
                    <li><strong>Access Your Tools</strong> - Timeline projector, manipulation detector, and more</li>
                </ul>

                <a href="{FRONTEND_URL}/bridge" class="button">Start Your Assessment</a>

                <p>If you have any questions, just reply to this email. We're here to help!</p>

                <p>Best regards,<br>
                The Consciousness Platform Team</p>
            </div>
            <div class="footer">
                <p>Consciousness Platform | Pattern Theory in Action</p>
                <p>You received this email because you signed up for an account.</p>
            </div>
        </div>
    </body>
    </html>
    """

    text_content = f"""
    Welcome to Consciousness Platform!

    Hi {display_name},

    Welcome to your journey of consciousness elevation! We're excited to have you join our community.

    What's Next?
    - Take the Consciousness Bridge Assessment - Discover your consciousness level in 3 minutes
    - Explore Pattern Theory - Learn to detect manipulation in real-time
    - Access Your Tools - Timeline projector, manipulation detector, and more

    Get started: {FRONTEND_URL}/bridge

    If you have any questions, just reply to this email. We're here to help!

    Best regards,
    The Consciousness Platform Team
    """

    return send_email(user_email, subject, html_content, text_content)


# ============= Assessment Results Email =============

def send_assessment_results_email(user_email: str, user_name: Optional[str],
                                   consciousness_level: float, level_name: str,
                                   percentile: int, top_domains: List[str]) -> tuple[bool, Optional[str]]:
    """Send consciousness assessment results"""

    display_name = user_name or user_email.split('@')[0]

    subject = f"Your Consciousness Assessment Results - {level_name}"

    domains_html = "".join([f"<li>{domain}</li>" for domain in top_domains[:3]])

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .score-box {{ background: white; border: 3px solid #667eea; border-radius: 10px;
                         padding: 20px; text-align: center; margin: 20px 0; }}
            .score {{ font-size: 48px; font-weight: bold; color: #667eea; }}
            .content {{ background: #f9f9f9; padding: 30px; }}
            .button {{ background: #667eea; color: white; padding: 12px 30px;
                      text-decoration: none; border-radius: 5px; display: inline-block;
                      margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Your Consciousness Assessment Results</h1>
            </div>
            <div class="content">
                <p>Hi {display_name},</p>

                <p>Congratulations on completing your Consciousness Bridge assessment! Here are your results:</p>

                <div class="score-box">
                    <div class="score">{int(consciousness_level)}</div>
                    <h2>{level_name}</h2>
                    <p>You're in the top {100 - percentile}% of consciousness levels</p>
                </div>

                <h3>Your Strongest Domains:</h3>
                <ul>
                    {domains_html}
                </ul>

                <p><strong>What This Means:</strong></p>
                <p>Your consciousness level reflects your current awareness across seven key domains of life.
                This is your baseline - and it can grow!</p>

                <h3>Recommended Next Steps:</h3>
                <ul>
                    <li>Explore the Pattern Theory Academy to deepen your understanding</li>
                    <li>Use the Manipulation Detector to sharpen your awareness</li>
                    <li>Join our community to connect with others on the same journey</li>
                </ul>

                <a href="{FRONTEND_URL}/results" class="button">View Full Results</a>

                <p>Keep growing!</p>

                <p>Best regards,<br>
                The Consciousness Platform Team</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(user_email, subject, html_content)


# ============= Subscription Emails =============

def send_subscription_confirmation_email(user_email: str, user_name: Optional[str],
                                         tier: str, amount: int) -> tuple[bool, Optional[str]]:
    """Send subscription confirmation email"""

    display_name = user_name or user_email.split('@')[0]

    tier_benefits = {
        'pro': [
            'Unlimited manipulation detections',
            'Unlimited timeline projections',
            'Full Pattern Theory Academy access',
            'Community posting privileges',
            'Priority email support'
        ],
        'enterprise': [
            'All Pro features',
            'API access (1000 requests/day)',
            'Custom pattern training',
            'White-label option',
            'Dedicated account manager',
            'SLA guarantee'
        ]
    }

    benefits = tier_benefits.get(tier, [])
    benefits_html = "".join([f"<li>{benefit}</li>" for benefit in benefits])

    subject = f"Welcome to Consciousness Platform {tier.capitalize()}! 🎉"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; }}
            .badge {{ background: #10b981; color: white; padding: 5px 15px;
                     border-radius: 20px; display: inline-block; font-weight: bold; }}
            .button {{ background: #667eea; color: white; padding: 12px 30px;
                      text-decoration: none; border-radius: 5px; display: inline-block;
                      margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Welcome to {tier.capitalize()}!</h1>
            </div>
            <div class="content">
                <p>Hi {display_name},</p>

                <p>Thank you for upgrading to <span class="badge">{tier.upper()}</span>!</p>

                <p>Your ${amount}/month subscription is now active and you have full access to:</p>

                <ul>
                    {benefits_html}
                </ul>

                <h3>Get Started:</h3>
                <p>All premium features are now unlocked in your account. Start exploring!</p>

                <a href="{FRONTEND_URL}/academy" class="button">Access Pattern Theory Academy</a>

                <p><strong>Manage Your Subscription:</strong></p>
                <p>You can update your payment method or cancel anytime from your account settings.</p>

                <p>Questions? Just reply to this email!</p>

                <p>Best regards,<br>
                The Consciousness Platform Team</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(user_email, subject, html_content)


def send_payment_failed_email(user_email: str, user_name: Optional[str]) -> tuple[bool, Optional[str]]:
    """Send payment failure notification"""

    display_name = user_name or user_email.split('@')[0]

    subject = "Payment Failed - Action Required"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #ef4444; color: white; padding: 30px;
                       text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; }}
            .button {{ background: #ef4444; color: white; padding: 12px 30px;
                      text-decoration: none; border-radius: 5px; display: inline-block;
                      margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⚠️ Payment Failed</h1>
            </div>
            <div class="content">
                <p>Hi {display_name},</p>

                <p>We were unable to process your recent payment for Consciousness Platform.</p>

                <p><strong>What happens now:</strong></p>
                <ul>
                    <li>Your subscription is currently past due</li>
                    <li>You still have access to premium features for the next 3 days</li>
                    <li>After 3 days, your account will revert to the free tier</li>
                </ul>

                <p><strong>To keep your premium access:</strong></p>
                <p>Please update your payment method in your account settings.</p>

                <a href="{FRONTEND_URL}/account/billing" class="button">Update Payment Method</a>

                <p>If you have questions or need assistance, just reply to this email.</p>

                <p>Best regards,<br>
                The Consciousness Platform Team</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(user_email, subject, html_content)


def send_subscription_canceled_email(user_email: str, user_name: Optional[str]) -> tuple[bool, Optional[str]]:
    """Send subscription cancellation confirmation"""

    display_name = user_name or user_email.split('@')[0]

    subject = "Subscription Canceled"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #6b7280; color: white; padding: 30px;
                       text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Subscription Canceled</h1>
            </div>
            <div class="content">
                <p>Hi {display_name},</p>

                <p>Your premium subscription has been canceled.</p>

                <p><strong>What this means:</strong></p>
                <ul>
                    <li>You'll have access to premium features until the end of your billing period</li>
                    <li>After that, your account will revert to the free tier</li>
                    <li>All your data and assessment results will be preserved</li>
                </ul>

                <p><strong>Free tier includes:</strong></p>
                <ul>
                    <li>Consciousness Bridge assessment</li>
                    <li>3 manipulation detections per month</li>
                    <li>Basic timeline projections</li>
                    <li>Community access (read-only)</li>
                </ul>

                <p>We're sorry to see you go! If you change your mind, you can resubscribe anytime from your account settings.</p>

                <p>Best regards,<br>
                The Consciousness Platform Team</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(user_email, subject, html_content)


# ============= Password Reset Email =============

def send_password_reset_email(user_email: str, reset_token: str) -> tuple[bool, Optional[str]]:
    """Send password reset link"""

    reset_link = f"{FRONTEND_URL}/reset-password?token={reset_token}"

    subject = "Reset Your Password"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; }}
            .button {{ background: #667eea; color: white; padding: 12px 30px;
                      text-decoration: none; border-radius: 5px; display: inline-block;
                      margin: 20px 0; }}
            .warning {{ background: #fef3c7; border-left: 4px solid #f59e0b;
                       padding: 15px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Reset Your Password</h1>
            </div>
            <div class="content">
                <p>We received a request to reset your password.</p>

                <p>Click the button below to create a new password:</p>

                <a href="{reset_link}" class="button">Reset Password</a>

                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #667eea;">{reset_link}</p>

                <div class="warning">
                    <strong>⚠️ Security Notice:</strong>
                    <ul>
                        <li>This link expires in 1 hour</li>
                        <li>If you didn't request this, ignore this email</li>
                        <li>Your password won't change unless you click the link</li>
                    </ul>
                </div>

                <p>Best regards,<br>
                The Consciousness Platform Team</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(user_email, subject, html_content)


# ============= Course Emails =============

def send_course_started_email(user_email: str, user_name: Optional[str],
                               course_title: str, lesson_count: int) -> tuple[bool, Optional[str]]:
    """Send email when user starts their first course in the academy"""
    display_name = user_name or user_email.split('@')[0]

    subject = f"Welcome to {course_title}! 🎯"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background: white;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: 600;
            }}
            .content {{
                padding: 40px 30px;
                background: #ffffff;
            }}
            .content h2 {{
                color: #667eea;
                font-size: 22px;
                margin-top: 0;
            }}
            .content p {{
                margin: 15px 0;
                color: #555;
            }}
            .stats {{
                background: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 15px 20px;
                margin: 20px 0;
            }}
            .stats strong {{
                color: #667eea;
            }}
            .tips {{
                background: #fff8e1;
                border-left: 4px solid #ffc107;
                padding: 15px 20px;
                margin: 20px 0;
            }}
            .tips h3 {{
                margin-top: 0;
                color: #f57c00;
                font-size: 16px;
            }}
            ul {{
                margin: 10px 0;
                padding-left: 20px;
            }}
            li {{
                margin: 8px 0;
                color: #555;
            }}
            .button {{
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 14px 32px;
                text-decoration: none;
                border-radius: 6px;
                margin: 25px 0;
                font-weight: 600;
                text-align: center;
            }}
            .button:hover {{
                background: #5568d3;
            }}
            .footer {{
                background: #f8f9fa;
                padding: 20px 30px;
                text-align: center;
                font-size: 14px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Your Learning Journey Begins! 🎯</h1>
            </div>
            <div class="content">
                <p>Hi {display_name},</p>

                <p>You've just started <strong>{course_title}</strong> in the Pattern Theory Academy. This is where consciousness elevation becomes systematic.</p>

                <div class="stats">
                    <strong>Course Overview:</strong><br>
                    📚 {lesson_count} lessons<br>
                    🎯 Practical exercises in every lesson<br>
                    ✅ Quizzes to test your understanding<br>
                    🏆 Track your progress as you master each domain
                </div>

                <h2>How to Get the Most from This Course</h2>

                <div class="tips">
                    <h3>Learning Tips:</h3>
                    <ul>
                        <li><strong>Don't rush</strong> - Pattern recognition develops with practice, not speed</li>
                        <li><strong>Do the exercises</strong> - Real-world application is where learning happens</li>
                        <li><strong>Take notes</strong> - Write down patterns you observe in your own life</li>
                        <li><strong>Return and review</strong> - Patterns become clearer on second viewing</li>
                        <li><strong>Apply immediately</strong> - Use what you learn the same day you learn it</li>
                    </ul>
                </div>

                <p><strong>Remember:</strong> Pattern Theory isn't just knowledge to consume - it's a skill to develop. Every lesson includes practical exercises designed to build your pattern recognition abilities in real situations.</p>

                <p>The goal isn't to "complete the course" - it's to <strong>transform how you see reality</strong>.</p>

                <a href="{FRONTEND_URL}/academy/courses/{course_title.lower().replace(' ', '-')}" class="button">Continue Learning →</a>

                <p>Questions or stuck on something? Reply to this email - we're here to help.</p>

                <p>Ready to elevate,<br>
                The Pattern Theory Academy Team</p>
            </div>
            <div class="footer">
                <p>Pattern Theory Academy | Consciousness Platform</p>
                <p>Track your progress: <a href="{FRONTEND_URL}/academy/progress">{FRONTEND_URL}/academy/progress</a></p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(user_email, subject, html_content)


def send_lesson_completed_email(user_email: str, user_name: Optional[str],
                                 course_title: str, lesson_title: str,
                                 quiz_score: Optional[float] = None) -> tuple[bool, Optional[str]]:
    """Send email when user completes a milestone lesson (with quiz)"""
    display_name = user_name or user_email.split('@')[0]

    subject = f"Lesson Complete: {lesson_title} ✅"

    score_section = ""
    if quiz_score is not None:
        score_percentage = int(quiz_score * 100)
        score_section = f"""
        <div class="stats">
            <strong>Your Quiz Score:</strong> {score_percentage}%<br>
            {'🎉 Excellent work!' if quiz_score >= 0.9 else '✅ Well done!' if quiz_score >= 0.7 else '📚 Consider reviewing and retaking'}
        </div>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background: white;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                color: white;
                padding: 40px 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: 600;
            }}
            .content {{
                padding: 40px 30px;
                background: #ffffff;
            }}
            .content p {{
                margin: 15px 0;
                color: #555;
            }}
            .stats {{
                background: #e8f5e9;
                border-left: 4px solid #4caf50;
                padding: 15px 20px;
                margin: 20px 0;
            }}
            .stats strong {{
                color: #2e7d32;
            }}
            .next-steps {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 6px;
                margin: 20px 0;
            }}
            .next-steps h3 {{
                margin-top: 0;
                color: #667eea;
            }}
            .button {{
                display: inline-block;
                background: #11998e;
                color: white;
                padding: 14px 32px;
                text-decoration: none;
                border-radius: 6px;
                margin: 25px 0;
                font-weight: 600;
                text-align: center;
            }}
            .footer {{
                background: #f8f9fa;
                padding: 20px 30px;
                text-align: center;
                font-size: 14px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Lesson Complete! ✅</h1>
            </div>
            <div class="content">
                <p>Hi {display_name},</p>

                <p>You've just completed <strong>"{lesson_title}"</strong> in {course_title}.</p>

                {score_section}

                <div class="next-steps">
                    <h3>What to Do Next:</h3>
                    <p><strong>1. Apply What You Learned</strong><br>
                    The real learning happens when you use these concepts in your actual life. Take the practical exercise seriously.</p>

                    <p><strong>2. Notice Patterns</strong><br>
                    For the next 24-48 hours, watch for examples of what you just learned appearing in your environment. Pattern recognition strengthens through observation.</p>

                    <p><strong>3. Continue the Journey</strong><br>
                    Each lesson builds on the previous ones. Keep the momentum going.</p>
                </div>

                <p><strong>Remember:</strong> Understanding the concept intellectually is step one. Recognizing it in real-time is mastery.</p>

                <a href="{FRONTEND_URL}/academy/courses/{course_title.lower().replace(' ', '-')}" class="button">Continue to Next Lesson →</a>

                <p>Keep building your consciousness,<br>
                The Pattern Theory Academy Team</p>
            </div>
            <div class="footer">
                <p>Pattern Theory Academy | Consciousness Platform</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(user_email, subject, html_content)


def send_course_completed_email(user_email: str, user_name: Optional[str],
                                 course_title: str, lessons_completed: int,
                                 next_course_title: Optional[str] = None) -> tuple[bool, Optional[str]]:
    """Send email when user completes entire course"""
    display_name = user_name or user_email.split('@')[0]

    subject = f"🎉 Course Complete: {course_title}"

    next_course_section = ""
    if next_course_title:
        next_course_section = f"""
        <div class="next-course">
            <h3>Ready for the Next Challenge?</h3>
            <p>Continue your pattern recognition journey with <strong>{next_course_title}</strong>.</p>
            <a href="{FRONTEND_URL}/academy" class="button">Start Next Course →</a>
        </div>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background: white;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                padding: 50px 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 32px;
                font-weight: 700;
            }}
            .header .trophy {{
                font-size: 64px;
                margin: 20px 0;
            }}
            .content {{
                padding: 40px 30px;
                background: #ffffff;
            }}
            .content p {{
                margin: 15px 0;
                color: #555;
                font-size: 16px;
            }}
            .achievement {{
                background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
                border-radius: 8px;
                padding: 25px;
                margin: 25px 0;
                text-align: center;
            }}
            .achievement h2 {{
                margin: 0 0 10px 0;
                color: #d84315;
                font-size: 24px;
            }}
            .achievement p {{
                margin: 5px 0;
                color: #555;
                font-size: 18px;
            }}
            .next-course {{
                background: #f8f9fa;
                padding: 25px;
                border-radius: 6px;
                margin: 25px 0;
            }}
            .next-course h3 {{
                margin-top: 0;
                color: #667eea;
            }}
            .reflection {{
                background: #e3f2fd;
                border-left: 4px solid #2196f3;
                padding: 20px;
                margin: 25px 0;
            }}
            .reflection h3 {{
                margin-top: 0;
                color: #1565c0;
                font-size: 18px;
            }}
            .button {{
                display: inline-block;
                background: #f5576c;
                color: white;
                padding: 14px 32px;
                text-decoration: none;
                border-radius: 6px;
                margin: 15px 0;
                font-weight: 600;
                text-align: center;
            }}
            .footer {{
                background: #f8f9fa;
                padding: 20px 30px;
                text-align: center;
                font-size: 14px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="trophy">🏆</div>
                <h1>Course Complete!</h1>
            </div>
            <div class="content">
                <p>Hi {display_name},</p>

                <p>Congratulations! You've completed <strong>{course_title}</strong>.</p>

                <div class="achievement">
                    <h2>Your Achievement</h2>
                    <p><strong>{lessons_completed} lessons completed</strong></p>
                    <p>Pattern recognition skills: <strong>ELEVATED</strong></p>
                </div>

                <p><strong>This isn't the end - it's the beginning.</strong></p>

                <p>You now have frameworks that most people will never see. The patterns you learned about aren't theoretical - they're operating all around you, every day. The difference is: now you can see them.</p>

                <div class="reflection">
                    <h3>Reflection Exercise:</h3>
                    <p>Before moving on, take 10 minutes to write down:</p>
                    <ul>
                        <li>What patterns have you started noticing in your daily life?</li>
                        <li>How has your perception of situations changed?</li>
                        <li>What will you do differently now that you see these patterns?</li>
                    </ul>
                    <p><strong>The writing is crucial.</strong> It transforms passive learning into active integration.</p>
                </div>

                {next_course_section}

                <p><strong>Remember:</strong> Pattern Theory mastery isn't about completing courses - it's about continuously refining your ability to see what others miss. Keep practicing.</p>

                <p>You're building something rare,<br>
                The Pattern Theory Academy Team</p>
            </div>
            <div class="footer">
                <p>Pattern Theory Academy | Consciousness Platform</p>
                <p>View your full progress: <a href="{FRONTEND_URL}/academy/progress">{FRONTEND_URL}/academy/progress</a></p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(user_email, subject, html_content)


# ============= Main (for testing) =============

if __name__ == "__main__":
    print("=" * 60)
    print("EMAIL SERVICE - Consciousness Platform")
    print("=" * 60)
    print(f"SendGrid configured: {'Yes' if sg else 'No'}")
    print(f"From: {SENDGRID_FROM_NAME} <{SENDGRID_FROM_EMAIL}>")
    print("\nAvailable email templates:")
    print("  - send_welcome_email()")
    print("  - send_assessment_results_email()")
    print("  - send_subscription_confirmation_email()")
    print("  - send_payment_failed_email()")
    print("  - send_subscription_canceled_email()")
    print("  - send_password_reset_email()")
    print("  - send_course_started_email()")
    print("  - send_lesson_completed_email()")
    print("  - send_course_completed_email()")
    print("=" * 60)
