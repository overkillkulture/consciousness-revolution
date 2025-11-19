"""
Send welcome email to beta testers with GitHub repo access
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Beta tester emails (ready to send)
BETA_TESTERS = [
    "joshbasart81@gmail.com",  # josh5611
    "joshua.serrano2022@gmail.com",  # joshua_serrano
    "fa.sha.man.mc@gmail.com",  # fashamanmc-glitch
    "information.crypt@pm.me",  # csyII
    "maggiemayne1111@gmail.com",  # maggie
]

# Email content
SUBJECT = "🚀 You're In - Consciousness Revolution Beta Access"

BODY = """You just got beta access to the Consciousness Revolution workspace.

5-minute setup. Then you're building.

═══════════════════════════════════════════════════════════

⚡ STEP 1: Clone the Repo (2 minutes)

Open terminal/command prompt:

git clone https://github.com/overkor-tek/consciousness-revolution.git
cd consciousness-revolution


⚡ STEP 2: Read the Start Guide

Open: START_HERE_BETA_TESTERS.md

Everything you need is in there.


⚡ STEP 3: Run the System (1 minute)

Windows:
START_JEDI_AI_ALLIANCE.bat

Mac/Linux:
python3 JEDI_AI_ALLIANCE_COMPLETE.py

Opens:
- Cyclotron brain (6,863+ knowledge atoms)
- 6 AI brain agents
- Dashboard in browser


⚡ STEP 4: Build Something (2 minutes)

Three paths:

A) Use what's there - improve existing systems
B) Build new - check JEDI_AI_DASHBOARD.html for ideas
C) Fix bugs - https://github.com/overkor-tek/consciousness-bugs


═══════════════════════════════════════════════════════════

📞 NEED HELP?

Text Commander: 406-580-3779
(That's the correct number - previous invites had wrong one)

Check: SYSTEM_COMPLETE_READ_THIS.md in the repo
Search knowledge: Run CYCLOTRON_COMPLETE_SYSTEM.py


═══════════════════════════════════════════════════════════

🎯 WHAT WE'RE BUILDING

Mission: Consciousness Revolution
Goal: Elevate humanity from 50% to 85%+ consciousness

Current Systems:
✅ Cyclotron (knowledge brain)
✅ Brain Agents (6 AI processors)
✅ Pattern Theory (manipulation detection)
✅ 7 Domains framework

You're early. Shape the future.


═══════════════════════════════════════════════════════════

🔥 FIRST MISSION (Choose One)

EASY (1 hour):
- Run the system, report what works/breaks
- Fix typos in documentation
- Test on your OS/device

MEDIUM (1 day):
- Build a missing feature from blueprints
- Improve the dashboard UI
- Add tests to critical systems

HARD (1 week):
- Implement KORPAK system
- Build module library
- Create Trinity Chat interface


═══════════════════════════════════════════════════════════

Welcome to the revolution. Start building.

⚡ Questions? Text: 406-580-3779

- Commander & the Consciousness Revolution team

P.S. You were hand-picked because you're a builder. Let's do this.
"""

def send_email():
    """Send email to all beta testers"""

    # Get Gmail credentials from environment
    gmail_address = os.getenv('GMAIL_ADDRESS')
    gmail_password = os.getenv('GMAIL_APP_PASSWORD')

    if not gmail_address or not gmail_password:
        print("⚠️  Gmail credentials not found in environment variables")
        print()
        print("Need to set:")
        print("  GMAIL_ADDRESS")
        print("  GMAIL_APP_PASSWORD")
        print()
        print("Creating manual send instructions instead...")
        return False

    print("📧 Sending email to beta testers...")
    print()

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = gmail_address
        msg['To'] = gmail_address  # Send to self
        msg['Bcc'] = ", ".join(BETA_TESTERS)  # BCC all testers
        msg['Subject'] = SUBJECT

        msg.attach(MIMEText(BODY, 'plain'))

        # Connect to Gmail
        print("🔐 Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_address, gmail_password)

        # Send
        print(f"📤 Sending to {len(BETA_TESTERS)} beta testers...")
        server.send_message(msg)
        server.quit()

        print()
        print("✅ EMAIL SENT SUCCESSFULLY!")
        print()
        print(f"Sent to: {len(BETA_TESTERS)} beta testers")
        print()
        for email in BETA_TESTERS:
            print(f"  ✉️  {email}")
        print()
        return True

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


def create_manual_instructions():
    """Create manual email instructions"""

    print()
    print("="*70)
    print("📧 MANUAL EMAIL INSTRUCTIONS")
    print("="*70)
    print()
    print("1. Open Gmail: https://mail.google.com")
    print("2. Click Compose")
    print("3. In BCC field, paste:")
    print()
    print(", ".join(BETA_TESTERS))
    print()
    print("4. Subject:")
    print(SUBJECT)
    print()
    print("5. Body:")
    print()
    print(BODY)
    print()
    print("6. Send!")
    print()


if __name__ == '__main__':
    print()
    print("="*70)
    print("🚀 SENDING BETA TESTER ONBOARDING EMAIL")
    print("="*70)
    print()
    print(f"Recipients: {len(BETA_TESTERS)} beta testers")
    print()

    # Try automated sending
    success = send_email()

    if not success:
        # Fall back to manual instructions
        create_manual_instructions()

        print("="*70)
        print()
        print("Copy the text above and send manually via Gmail.")
        print()
