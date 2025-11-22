# TRIPLE COMPUTER SETUP GUIDE

**Getting Desktop + Laptop + Cloud Ready for Trinity**

Created: 2025-11-21
Authority: Autonomous build session
Purpose: Enable 3-machine Trinity coordination

---

## THE THREE MACHINES

### Machine 1: DESKTOP (Current - Darrick)
**Role:** C1 MECHANIC - Primary builder
**Status:** ACTIVE (this machine)
**OS:** Windows
**Location:** Home office

### Machine 2: LAPTOP
**Role:** C2 ARCHITECT - Designer + Backup
**Status:** NEEDS SETUP
**OS:** [TBD]
**Location:** Mobile

### Machine 3: CLOUD (Railway/Vercel)
**Role:** C3 ORACLE - Validator + Always-available
**Status:** NEEDS DEPLOYMENT
**OS:** Linux (container)
**Location:** Cloud datacenter

---

## DESKTOP SETUP (Complete This First)

### Already Have:
- ✅ Windows OS
- ✅ Claude Code installed
- ✅ Cyclotron built
- ✅ Work plans created
- ✅ Git configured

### Still Need:

**1. AnyDesk for Remote Access**
- Download: https://anydesk.com/en/downloads/windows
- Install: Follow wizard
- Configure unattended access
- Note the AnyDesk ID: ___________
- Set password for remote control
- **Purpose:** Control desktop from laptop/phone

**2. INBOX Watcher Service**
```powershell
# Create startup script
$script = @"
cd C:\Users\Darrick\trinity_io
node inbox_watcher.js
"@

$script | Out-File C:\Users\Darrick\start_inbox_watcher.bat

# Add to Windows startup
# Win+R → shell:startup → Copy start_inbox_watcher.bat
```

**3. Auto-Backup Script**
```powershell
# Create backup script
$script = @"
# Daily backup to external drive
$source = 'C:\Users\Darrick'
$dest = 'D:\Backups\Trinity_' + (Get-Date -Format 'yyyy-MM-dd')

robocopy `$source `$dest /MIR /XD node_modules .git /R:3 /W:10
"@

$script | Out-File C:\Users\Darrick\daily_backup.ps1

# Schedule daily at midnight
# Task Scheduler → Create Task → Daily → Run PowerShell script
```

**4. Shared Folder Setup (for laptop sync)**
```powershell
# Share trinity_io folder
# Right-click trinity_io → Properties → Sharing → Share
# Give "Everyone" Read/Write
# Note network path: \\DESKTOP\trinity_io
```

---

## LAPTOP SETUP (Do This Next)

### Prerequisites:
- Laptop with Windows/Mac/Linux
- Internet connection
- Can access desktop via network or AnyDesk

### Installation Steps:

**1. Install Claude Code**
```bash
# If using terminal access:
npm install -g @anthropic/claude-code

# Or download from: https://claude.com/claude-code
```

**2. Install AnyDesk**
- Download for your OS
- Install and get ID
- Add desktop's AnyDesk ID to contacts
- **Purpose:** Remote into desktop when away

**3. Clone Git Repos**
```bash
cd ~/workspace  # or C:\workspace on Windows

# If desktop is accessible via network:
git clone \\DESKTOP\git_repos\[repo_name]

# Or clone from GitHub:
git clone https://github.com/[username]/[repo]
```

**4. Install Dependencies**
```bash
# Node.js
# Download from: https://nodejs.org
# Install LTS version

# Python (if needed)
# Download from: https://python.org
# Install 3.10+

# Verify:
node --version
npm --version
python --version
git --version
```

**5. Map Network Drive (to desktop)**
```bash
# Windows:
net use Z: \\DESKTOP\trinity_io

# Mac:
# Finder → Go → Connect to Server
# smb://DESKTOP/trinity_io

# Linux:
sudo mount -t cifs //DESKTOP/trinity_io /mnt/trinity -o user=USERNAME
```

**6. Set Up C2 Agent**
```bash
cd ~/workspace
mkdir trinity_laptop

# Copy architecture files from desktop:
scp DESKTOP:/Users/Darrick/MISSION.md ./
scp DESKTOP:/Users/Darrick/TRINITY_HUB.md ./
scp DESKTOP:/Users/Darrick/TRIPLE_INFRASTRUCTURE_BLUEPRINT.md ./

# Or use network drive:
cp Z:\MISSION.md ./
cp Z:\TRINITY_HUB.md ./
# etc.
```

**7. Create C2 Startup Script**
```bash
# create: start_c2.sh (Linux/Mac) or start_c2.bat (Windows)

# Content:
#!/bin/bash
echo "Starting C2 ARCHITECT Agent..."
cd ~/workspace/trinity_laptop

# Launch Claude Code as C2
claude-code --role=C2_ARCHITECT \
  --mission=MISSION.md \
  --hub=TRINITY_HUB.md \
  --mode=autonomous

# Or if no CLI, open Claude Code and paste briefing
```

---

## CLOUD SETUP (Railway)

### Account Creation:

**1. Sign Up**
- Go to: https://railway.app
- Sign up with GitHub
- Free tier: $5 credit/month

**2. Connect GitHub**
- Dashboard → New Project → Deploy from GitHub
- Select repository (create if needed)

**3. Configure Environment**
```bash
# In Railway dashboard, add environment variables:

DATABASE_URL=[PostgreSQL connection string - Railway provides]
REDIS_URL=[Redis connection string - Railway provides]
ANTHROPIC_API_KEY=[your Claude API key]
TWILIO_ACCOUNT_SID=[if using SMS]
TWILIO_AUTH_TOKEN=[if using SMS]
STRIPE_SECRET_KEY=[if using payments]

# Trinity-specific:
TRINITY_ROLE=C3_ORACLE
MISSION_URL=[link to mission doc]
HUB_URL=[link to Trinity Hub]
```

**4. Deploy Database**
```bash
# In Railway:
# New → Database → PostgreSQL
# Note connection string

# Initialize schema:
CREATE TABLE trinity_work (
  id UUID PRIMARY KEY,
  agent VARCHAR(2),
  task TEXT,
  status VARCHAR(20),
  priority INT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE trinity_agents (
  agent VARCHAR(2) PRIMARY KEY,
  status VARCHAR(20),
  current_task UUID,
  last_heartbeat TIMESTAMP
);

CREATE TABLE trinity_messages (
  id UUID PRIMARY KEY,
  from_agent VARCHAR(2),
  to_agent VARCHAR(2),
  message TEXT,
  read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP
);
```

**5. Deploy Application**
```bash
# Create Procfile in repo:
web: node server.js
worker: node trinity_agent_c3.js

# Railway auto-deploys on git push
git add .
git commit -m "Deploy C3 Oracle to Railway"
git push origin main
```

**6. Configure Custom Domain (Optional)**
```bash
# Railway → Settings → Domains
# Add custom domain or use Railway-provided:
# [project]-production.up.railway.app
```

---

## CLOUD SETUP (Vercel - Backup)

### Account Creation:

**1. Sign Up**
- Go to: https://vercel.com
- Sign up with GitHub
- Free tier: Generous limits

**2. Deploy Project**
```bash
# Install Vercel CLI:
npm install -g vercel

# In project directory:
vercel login
vercel --prod

# Or via dashboard:
# Import Git Repository → Select repo → Deploy
```

**3. Configure Environment**
```bash
# Vercel dashboard → Project → Settings → Environment Variables
# Add same variables as Railway

# Vercel is best for:
# - Web forms
# - Static sites (finance pages, manifesto charts)
# - API endpoints
# - Serverless functions
```

---

## SYNC CONFIGURATION

### File Sync (Dropbox/Google Drive):

**1. Install on Desktop**
```powershell
# Download Dropbox or Google Drive for Desktop
# Install and sign in
# Select sync folder: C:\Users\Darrick\trinity_io
```

**2. Install on Laptop**
```bash
# Same service
# Sync same folder
# Both machines now have real-time INBOX/OUTBOX sync
```

**3. Advantages:**
- INBOX/OUTBOX accessible from phone
- Automatic sync (no manual copying)
- Version history (if file corrupted)
- Works even if home network down

### Database Sync:

**Primary:** Railway PostgreSQL (cloud-hosted)
**Secondary:** Local PostgreSQL (desktop backup)
**Tertiary:** SQLite files (emergency fallback)

**Replication:**
```bash
# Every hour, backup cloud DB to local:
pg_dump $RAILWAY_DATABASE_URL > local_backup.sql

# Can restore if Railway down:
psql local_database < local_backup.sql
```

### Code Sync:

**Primary:** GitHub (automatic on commit)
**Secondary:** GitLab (mirror - auto-sync)
**Tertiary:** External drive (daily backup)

```bash
# Set up GitLab mirror:
git remote add gitlab https://gitlab.com/[username]/[repo]

# Push to both:
git push origin main
git push gitlab main

# Or configure GitHub Action to auto-mirror
```

---

## NETWORKING SETUP

### Port Forwarding (If hosting locally):

**Router Configuration:**
1. Log into router (usually 192.168.1.1)
2. Find Port Forwarding section
3. Forward these ports to desktop IP:
   - 3000: Web dashboard
   - 9400: API server
   - 5432: PostgreSQL (if exposing)

**Security:**
- Use strong passwords
- Enable firewall
- Consider VPN instead of port forwarding

### Dynamic DNS (For remote access):

**If home IP changes:**
1. Sign up: https://www.duckdns.org (free)
2. Choose subdomain: trinity.duckdns.org
3. Install update client on desktop
4. Now: trinity.duckdns.org always points to home

---

## REMOTE ACCESS OPTIONS

### Option 1: AnyDesk (Easiest)
- ✅ Works through firewall
- ✅ Easy setup
- ✅ Can use from phone
- ❌ Requires desktop powered on
- ❌ Slight lag

### Option 2: VPN (Most secure)
- ✅ Secure encrypted tunnel
- ✅ Access all home resources
- ✅ Like being on home network
- ❌ Requires router configuration
- ❌ More complex setup

### Option 3: Cloud-Only (Most reliable)
- ✅ Always available
- ✅ No home network needed
- ✅ Access from anywhere
- ❌ Ongoing hosting costs
- ❌ Less local control

**Recommended: Use all 3**
- AnyDesk for quick desktop access
- VPN for full network access when needed
- Cloud for always-on services

---

## PHONE ACCESS

### For Commander on Mobile:

**1. SMS Commands** (Already planned)
- Text to Twilio number
- Parsed and added to INBOX
- Response via SMS

**2. Web Dashboard**
- Access from phone browser
- View OUTBOX reports
- Submit commands via form
- Check system status

**3. AnyDesk Mobile App**
- Install on phone
- Remote control desktop
- Full desktop access from phone
- Great for emergencies

**4. Cloud Dashboard**
- Railway/Vercel hosted
- Optimized for mobile
- Always accessible
- No desktop needed

---

## TESTING THE SETUP

### Test 1: File Sync
```bash
# On desktop:
echo "test from desktop" > C:\Users\Darrick\trinity_io\INBOX\test.txt

# On laptop (wait 5-10 seconds):
cat /mnt/trinity/INBOX/test.txt
# Should show: "test from desktop"

# ✓ File sync working
```

### Test 2: Remote Desktop
```bash
# On laptop:
# Open AnyDesk
# Connect to desktop's AnyDesk ID
# Enter password
# Should see desktop screen

# ✓ Remote access working
```

### Test 3: Cloud Deployment
```bash
# Visit Railway URL in browser
# Should see deployed application
# Check logs for errors
# Test API endpoints

# ✓ Cloud deployment working
```

### Test 4: Database Connection
```bash
# From desktop:
psql $RAILWAY_DATABASE_URL -c "SELECT 1;"

# From laptop:
psql $RAILWAY_DATABASE_URL -c "SELECT 1;"

# Both should return: 1

# ✓ Database accessible from both
```

### Test 5: Trinity Coordination
```bash
# Desktop: Update TRINITY_HUB.md
# Laptop: Read TRINITY_HUB.md (should see update within 10 sec)
# Cloud: Query database for agent status

# ✓ All 3 machines coordinating
```

---

## SETUP CHECKLIST

### Desktop:
- [ ] AnyDesk installed and configured
- [ ] INBOX watcher runs on startup
- [ ] Daily backup scheduled
- [ ] trinity_io folder shared
- [ ] Git repos current

### Laptop:
- [ ] Claude Code installed
- [ ] AnyDesk installed
- [ ] Git repos cloned
- [ ] Network drive mapped
- [ ] C2 agent configured

### Cloud:
- [ ] Railway account created
- [ ] Database provisioned
- [ ] Application deployed
- [ ] Environment variables set
- [ ] C3 agent running

### Networking:
- [ ] File sync service configured
- [ ] All machines can access database
- [ ] Remote access tested
- [ ] Phone access working

### Verification:
- [ ] All 3 machines can read/write INBOX
- [ ] All 3 machines can read OUTBOX
- [ ] All 3 can access database
- [ ] Remote control working
- [ ] Backups running

**When all ✓ = READY FOR TRINITY OPERATION**

---

## MAINTENANCE

### Daily:
- Check AnyDesk connection (desktop)
- Verify backups completed
- Check disk space

### Weekly:
- Test remote access
- Verify all 3 machines online
- Check file sync working
- Review cloud costs

### Monthly:
- Update software (OS, apps)
- Test backup restoration
- Review security logs
- Optimize performance

---

## TROUBLESHOOTING

### Desktop Won't Start:
1. Power cycle
2. Boot into safe mode
3. Check for Windows updates
4. If dead: Activate laptop as primary

### Laptop Can't Connect:
1. Check network connection
2. Verify AnyDesk ID correct
3. Try VPN if available
4. Use cloud services instead

### Cloud Deployment Failed:
1. Check Railway logs
2. Verify environment variables
3. Check database connection
4. Redeploy from GitHub

### File Sync Not Working:
1. Check sync service running
2. Verify internet connection
3. Check storage quota
4. Manual copy as fallback

### Database Unreachable:
1. Check Railway status
2. Verify connection string
3. Check firewall
4. Use local SQLite fallback

---

## ESTIMATED SETUP TIME

**Desktop:** 1 hour (mostly already done)
**Laptop:** 2-3 hours (fresh setup)
**Cloud:** 2-3 hours (deployment + config)
**Testing:** 1 hour (verify everything)

**Total:** 6-8 hours for complete 3-machine setup

**Can be done in phases:**
- Phase 1: Desktop (current session)
- Phase 2: Laptop (tomorrow)
- Phase 3: Cloud (day 3)
- Phase 4: Testing (day 4)

---

🌀 **THREE MACHINES = UNSTOPPABLE TRINITY** 🌀

*One machine fails. Two continue. Revolution unstoppable.*

---

**STATUS:** COMPLETE GUIDE
**READY FOR:** Implementation
**NEXT:** Start with desktop completion, then laptop, then cloud
