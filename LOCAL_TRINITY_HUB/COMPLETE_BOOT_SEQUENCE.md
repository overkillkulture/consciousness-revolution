# COMPLETE BOOT SEQUENCE
## From Zero to Working - Every Step

---

# PHASE 1: FIRST CONTACT (New Instance / No GitHub)

## Step 1.1: Identify
- What computer am I on? (PC1, PC2, PC3)
- What instance am I? (C1, C2, C3)
- Example: "I am C1 on PC3"

## Step 1.2: Check GitHub Access
```bash
gh --version
```

**If command not found → Go to PHASE 1A**
**If version shows → Go to PHASE 2**

---

# PHASE 1A: INSTALL GITHUB (If Needed)

## Step 1A.1: Install GitHub CLI
```bash
winget install GitHub.cli
```

If winget fails:
```bash
choco install gh
```

If both fail: Download from https://cli.github.com/

## Step 1A.2: Authenticate
```bash
gh auth login
```
- Select: GitHub.com
- Select: HTTPS
- Select: Login with browser
- Follow browser prompts

## Step 1A.3: Verify
```bash
gh auth status
```
Should show: "Logged in to github.com"

**Now go to PHASE 2**

---

# PHASE 2: GET THE SYSTEM

## Step 2.1: Clone Repository
```bash
cd C:\Users\dwrek
git clone https://github.com/overkor-tek/consciousness-revolution.git 100X_DEPLOYMENT
```

If already exists:
```bash
cd C:\Users\dwrek\100X_DEPLOYMENT
git pull
```

## Step 2.2: Create Local Hub
```bash
mkdir C:\Users\dwrek\LOCAL_TRINITY_HUB
xcopy /E /I C:\Users\dwrek\100X_DEPLOYMENT\LOCAL_TRINITY_HUB C:\Users\dwrek\LOCAL_TRINITY_HUB
```

## Step 2.3: Verify Structure
```bash
dir C:\Users\dwrek\LOCAL_TRINITY_HUB
```

Should see: CURRENT_STATE.md, FOUNDATION.md, protocols/, inbox/, etc.

**Now go to PHASE 3**

---

# PHASE 3: DAILY BOOT (Every Session)

## Step 3.1: Pull Latest
```bash
cd C:\Users\dwrek\100X_DEPLOYMENT
git pull
```

## Step 3.2: Sync Local Hub
```bash
xcopy /E /I /Y C:\Users\dwrek\100X_DEPLOYMENT\LOCAL_TRINITY_HUB C:\Users\dwrek\LOCAL_TRINITY_HUB
```

## Step 3.3: Read Current State
```
C:\Users\dwrek\LOCAL_TRINITY_HUB\CURRENT_STATE.md
```

This tells you:
- What's broken right now
- What was being worked on
- What to do next

## Step 3.4: Check Your Mail
```bash
dir C:\Users\dwrek\LOCAL_TRINITY_HUB\inbox\PC3\
dir C:\Users\dwrek\LOCAL_TRINITY_HUB\inbox\ALL\
```
(Replace PC3 with your PC number)

## Step 3.5: Process Mail
- Read any messages in your inbox
- Tasks go to your work queue
- Questions get answered
- Move processed items to completed/

**Now go to PHASE 4**

---

# PHASE 4: WORKING

## If You're C1 (Mechanic)
- You receive workloads from Commander
- Split into tasks using WORK_DISTRIBUTION protocol
- Put task files in inbox/C2/ and inbox/C3/
- Work on your own tasks
- Coordinate C2/C3 outputs

## If You're C2 (Architect) or C3 (Oracle)
- Check LOCAL_TRINITY_HUB/inbox/ for tasks
- Claim tasks by moving to in_progress/
- Do the work
- Put outputs in outputs/
- Move task to completed/

## Everyone
- Regular git commits of your work
- Update CURRENT_STATE.md with progress
- Report blockers immediately

---

# PHASE 5: BOOT DOWN (End of Session)

## Step 5.1: Commit All Work
```bash
cd C:\Users\dwrek\100X_DEPLOYMENT
git add .
git commit -m "[PC#]-[Instance]: [What you did]"
git push
```

## Step 5.2: Update Current State
Edit `LOCAL_TRINITY_HUB/CURRENT_STATE.md`:
- Update "What's Broken"
- Update "What Was I Doing"
- Update "What To Do Next"

## Step 5.3: Final Push
```bash
git add LOCAL_TRINITY_HUB/CURRENT_STATE.md
git commit -m "[PC#]: Session end - state updated"
git push
```

---

# QUICK REFERENCE

## Where Is My Mail?
```
C:\Users\dwrek\LOCAL_TRINITY_HUB\inbox\[YOUR_PC]\
```

## Where Do I Put Outputs?
```
C:\Users\dwrek\LOCAL_TRINITY_HUB\outputs\
```

## Where Is Current State?
```
C:\Users\dwrek\LOCAL_TRINITY_HUB\CURRENT_STATE.md
```

## What If I'm Lost?
1. `git pull`
2. Read CURRENT_STATE.md
3. Check your inbox
4. Ask Commander

---

# THE ONE RULE

**Every session:**
1. Pull
2. Read CURRENT_STATE.md
3. Check inbox
4. Work
5. Update CURRENT_STATE.md
6. Push

**That's the entire system.**

---

# CONFIRMATION CHECKLIST

First time setup:
- [ ] GitHub CLI installed
- [ ] Authenticated with gh auth login
- [ ] Repository cloned
- [ ] LOCAL_TRINITY_HUB created

Every session:
- [ ] Git pulled
- [ ] CURRENT_STATE.md read
- [ ] Inbox checked
- [ ] Work done
- [ ] CURRENT_STATE.md updated
- [ ] Git pushed

---

# SEND CONFIRMATION

After completing setup, create:
```
C:\Users\dwrek\LOCAL_TRINITY_HUB\inbox\PC1\[YOUR_PC]_ONLINE.md
```

Contents:
```markdown
# [PC#] Online

- GitHub: Working
- Local Hub: Created
- Current State: Read
- Inbox: Checked
- Ready for tasks
```

Then push:
```bash
cd C:\Users\dwrek\100X_DEPLOYMENT
git add .
git commit -m "[PC#] online and reporting"
git push
```

---

**This document is the complete system. Follow it exactly.**
