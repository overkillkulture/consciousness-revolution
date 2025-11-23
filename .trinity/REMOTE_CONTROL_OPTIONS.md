# 🖥️ Screen Sharing & Remote Control Options for Trinity

## Overview

Remote control enables:
- Phone → trigger computers
- Computer → control other computers
- Desktop Claude → control UI (via Magic Mouse)
- Visual monitoring of all PCs

---

## TIER 1: Already Have / Easy Setup

### 1. Tailscale (Network Layer)
**Status:** Already installed on some systems

**What it does:**
- Creates secure mesh network between all devices
- Each device gets stable IP (100.x.x.x)
- Works through firewalls/NAT

**Trinity Use:**
- Direct communication between PCs
- SSH access to any PC
- File sharing via network paths

**Setup:**
```bash
# Each PC
tailscale up
tailscale status  # Get IPs
```

**Integration:**
```python
# Direct HTTP between PCs
PC1_IP = "100.64.0.1"
PC2_IP = "100.64.0.2"
requests.post(f"http://{PC2_IP}:8888/wake", json={"task": "..."})
```

---

### 2. AnyDesk
**Status:** May already have

**What it does:**
- Full remote desktop control
- Works without port forwarding
- Phone app available

**Trinity Use:**
- Visual monitoring from phone
- Emergency intervention
- See what each PC is doing

**Setup:**
- Install AnyDesk on each PC
- Note the AnyDesk ID
- Set unattended access password

**Phone Integration:**
- Install AnyDesk app
- Connect to any PC by ID
- Visual monitoring while away

---

### 3. Windows Remote Desktop (RDP)
**Status:** Built into Windows

**What it does:**
- Full desktop control
- Optimized for Windows
- Requires network access

**Trinity Use:**
- Computer-to-computer control
- Works great over Tailscale

**Setup:**
```
Settings → System → Remote Desktop → Enable
```

**Connection:**
```
mstsc /v:PC2-tailscale-ip
```

---

## TIER 2: Programmatic Control

### 4. SSH + Python
**What it does:**
- Command-line access to any PC
- Run scripts remotely
- No GUI needed

**Trinity Use:**
- Best for automated commands
- Wake scripts, git operations
- Lightweight

**Setup (Windows):**
```powershell
# Enable OpenSSH Server
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.67.1
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
```

**Usage:**
```python
import paramiko

def run_on_pc2(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('100.64.0.2', username='dwrek', password='...')
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode()

# Wake PC2's Trinity
run_on_pc2('python .trinity/automation/START_TRINITY_SYSTEM.bat')
```

---

### 5. PyAutoGUI (Mouse/Keyboard Control)
**What it does:**
- Programmatic mouse/keyboard control
- Can click buttons, type text
- Screenshot capability

**Trinity Use:**
- Desktop Claude controlling UI
- Automating browser actions
- "Magic Mouse" functionality

**Setup:**
```bash
pip install pyautogui pillow
```

**Usage:**
```python
import pyautogui

# Click coordinates
pyautogui.click(100, 200)

# Type text
pyautogui.write('hello')

# Screenshot
screenshot = pyautogui.screenshot()

# Find image on screen and click
location = pyautogui.locateOnScreen('button.png')
if location:
    pyautogui.click(location)
```

**Desktop Claude Integration:**
```python
class DesktopAutomation:
    def spawn_cloud_code(self):
        # Open Claude menu
        pyautogui.click(50, 50)
        time.sleep(0.5)
        # Click "New Project"
        pyautogui.click(100, 150)

    def open_terminal(self):
        pyautogui.hotkey('ctrl', '`')

    def git_pull(self):
        self.open_terminal()
        pyautogui.write('git pull')
        pyautogui.press('enter')
```

---

### 6. VNC (Virtual Network Computing)
**What it does:**
- Screen sharing protocol
- Cross-platform
- Multiple viewer options

**Trinity Use:**
- Lightweight remote viewing
- Works with Tailscale

**Server (TightVNC):**
```
Download and install TightVNC Server
Set password
Runs on port 5900
```

**Viewer:**
```
Connect to: 100.64.0.2:5900
```

---

## TIER 3: Advanced Options

### 7. Parsec
**What it does:**
- Low-latency remote desktop
- Gaming-grade performance
- Great for visual work

**Trinity Use:**
- When you need smooth visual monitoring
- Phone viewing with minimal lag

---

### 8. Chrome Remote Desktop
**What it does:**
- Browser-based remote access
- Easy setup
- Works from any device

**Trinity Use:**
- Quick access from phone browser
- No app installation needed

---

### 9. Synergy/Barrier
**What it does:**
- Share mouse/keyboard across computers
- Not remote control, but side-by-side control

**Trinity Use:**
- If all 3 PCs are on your desk
- Single keyboard controls all

---

## Recommended Stack for Trinity

### Minimum Viable:
1. **Tailscale** - Network connectivity
2. **SSH** - Command execution
3. **Git** - State synchronization

### Enhanced Control:
4. **AnyDesk** - Visual monitoring from phone
5. **PyAutoGUI** - Desktop Claude UI control

### Full Automation:
6. **VNC** - Lightweight visual access
7. **Custom HTTP APIs** - Direct PC-to-PC communication

---

## Implementation Priority

### Phase 1: Network Foundation
```
1. Install Tailscale on all 3 PCs
2. Get stable IPs
3. Test connectivity: ping between PCs
4. Enable SSH on all PCs
```

### Phase 2: Automated Control
```
1. Install PyAutoGUI on all PCs
2. Create basic automation scripts
3. Test: one PC controls another via SSH
4. Build: wake_via_ssh.py
```

### Phase 3: Visual Monitoring
```
1. Install AnyDesk on all PCs
2. Install AnyDesk on phone
3. Test: view PC from phone
4. Document AnyDesk IDs
```

### Phase 4: Full Integration
```
1. HTTP API on each PC for Trinity commands
2. Dashboard showing all PC screens
3. One-click control panel
```

---

## Quick Win: SSH Wake Script

```python
# WAKE_VIA_SSH.py
import paramiko
import os

COMPUTERS = {
    "PC1": {"ip": "100.64.0.1", "user": "dwrek"},
    "PC2": {"ip": "100.64.0.2", "user": "dwrek"},
    "PC3": {"ip": "100.64.0.3", "user": "dwrek"}
}

def wake_computer(pc_id, task):
    """SSH into computer and run wake script"""
    pc = COMPUTERS[pc_id]

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(pc["ip"], username=pc["user"], key_filename="~/.ssh/id_rsa")

    # Run the wake command
    command = f'cd 100X_DEPLOYMENT && git pull && python .trinity/automation/START_TRINITY_SYSTEM.bat'
    stdin, stdout, stderr = ssh.exec_command(command)

    print(f"Woke {pc_id}: {stdout.read().decode()}")
    ssh.close()

def wake_all(task):
    """Wake all computers"""
    for pc_id in COMPUTERS:
        wake_computer(pc_id, task)

if __name__ == "__main__":
    wake_all("Execute spawn queue")
```

---

## Desktop Claude + PyAutoGUI Bridge

The "Magic Mouse" concept - Desktop Claude controlling UI:

```python
# DESKTOP_CLAUDE_HANDS.py
import pyautogui
import time

class DesktopHands:
    """Gives Desktop Claude hands to interact with UI"""

    def __init__(self):
        pyautogui.FAILSAFE = True  # Move mouse to corner to stop
        self.screen_width, self.screen_height = pyautogui.size()

    def click_button(self, button_image):
        """Find and click a button by image"""
        location = pyautogui.locateOnScreen(button_image, confidence=0.9)
        if location:
            pyautogui.click(pyautogui.center(location))
            return True
        return False

    def open_browser_url(self, url):
        """Open URL in browser"""
        pyautogui.hotkey('win', 'r')
        time.sleep(0.5)
        pyautogui.write(f'chrome {url}')
        pyautogui.press('enter')

    def spawn_terminal(self):
        """Open new terminal"""
        pyautogui.hotkey('win', 'r')
        time.sleep(0.3)
        pyautogui.write('cmd')
        pyautogui.press('enter')

    def type_in_terminal(self, command):
        """Type command in active terminal"""
        pyautogui.write(command)
        pyautogui.press('enter')

    def take_screenshot(self, filename):
        """Screenshot for verification"""
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)

    def wait_for_element(self, image, timeout=30):
        """Wait for UI element to appear"""
        start = time.time()
        while time.time() - start < timeout:
            if pyautogui.locateOnScreen(image, confidence=0.8):
                return True
            time.sleep(1)
        return False
```

---

## Summary

**For Trinity coordination, the recommended stack is:**

1. **Tailscale** - Secure network between all devices
2. **SSH** - Automated command execution
3. **Git** - State sync (already using)
4. **PyAutoGUI** - Desktop Claude UI control
5. **AnyDesk** - Visual monitoring from phone

This gives you:
- Phone can trigger any PC
- PCs can control each other
- Desktop Claude can interact with UI
- Visual monitoring when needed
- All without exposing to internet
