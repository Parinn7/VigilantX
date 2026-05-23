# VigilantX 🛡️
**Security Monitoring System — Internship Project**
*Forensic CyberTec | Security Engineering Intern*

---

## About
VigilantX is a two-layer security monitoring system I built during my internship at Forensic CyberTec. It monitors login activity and file integrity in real-time, sending email alerts to both the security team and clients when suspicious activity is detected.

---

## What it does

**LogHound** — monitors login logs and detects:
- Brute force attacks (10+ failed logins within 5 minutes)
- Logins from new IP addresses
- Logins from new geographic locations

**IntegrityX** — monitors a folder and detects:
- Any file created, modified, deleted or renamed
- Ransomware-like behavior (10+ files changing rapidly)

**Notifications** — sends email alerts:
- Admin gets full technical details
- Client gets a simple plain English summary

---

## Project Structure
```
VigilantX/
├── LogHound/
│   ├── failed_logins.py      → brute force detection
│   ├── new_ip.py             → new IP login detection
│   ├── new_location.py       → new location login detection
│   └── log_analyzer.py       → runs all 3 detectors together
├── IntegrityX/
│   └── file_monitor.py       → file change + ransomware detection
├── Notifications/
│   ├── admin_alert.py        → technical email alerts to admin
│   └── client_alert.py       → simple email alerts to client
├── logs/
│   ├── auth.log              → login activity logs
│   └── generate_logs.py      → fake log generator for testing
├── test_files/               → folder watched by IntegrityX
└── .env                      → credentials (never push this!)
```

---

## Setup

**1 — Clone and enter the project**
```bash
git clone https://github.com/yourusername/VigilantX.git
cd VigilantX
```

**2 — Create and activate virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3 — Install dependencies**
```bash
pip install watchdog flask pandas python-dotenv
```

**4 — Create a .env file in the root folder**
```
SENDER_EMAIL=yourgmail@gmail.com
SENDER_PASSWORD=xxxxxxxxxxxxxxxx
ADMIN_EMAIL=admin@example.com
CLIENT_EMAIL=client@example.com
```

> SENDER_PASSWORD is a Gmail App Password, not your regular password.
> Get one here: Google Account → Security → 2-Step Verification → App Passwords

---

## Running

```bash
# Activate venv every time you open a new terminal
source .venv/bin/activate

# Generate fake logs for testing
python3 logs/generate_logs.py

# Run LogHound only
python3 LogHound/log_analyzer.py

# Run IntegrityX only
python3 IntegrityX/file_monitor.py
```

---

## Testing

**Generate fake logs**
```bash
python3 logs/generate_logs.py
```
This creates fake login logs with 3 scenarios already planted:
- 15 failed logins from Russia (brute force)
- New IP login from Brazil
- New location login from China

**Run LogHound and see all 3 detections**
```bash
python3 LogHound/log_analyzer.py
```

**Test single file change detection**
Open two terminals. In terminal 1 start IntegrityX:
```bash
python3 IntegrityX/file_monitor.py
```
In terminal 2 make a file change:
```bash
echo "test" >> test_files/document1.txt
```

**Test file creation detection**
In terminal 2 while IntegrityX is running:
```bash
touch test_files/newfile.txt
```

**Test file deletion detection**
In terminal 2 while IntegrityX is running:
```bash
rm test_files/document2.txt
```

**Test ransomware detection**
In terminal 2 while IntegrityX is running:
```bash
for i in {1..15}; do touch test_files/ransomware_test_$i.txt; done
```
IntegrityX will detect 10+ rapid file changes and trigger a ransomware alert.

**Test email notifications**
Add a test alert at the bottom of admin_alert.py:
if __name__ == "__main__":
    test_alert = {
        "type": "BRUTE_FORCE",
        "user": "admin",
        "ip": "45.33.32.156",
        "location": "Russia",
        "count": 15,
        "severity": "HIGH",
        "time": "2026-05-20 17:04:13"
    }
    send_admin_alert(test_alert) 
    

and run:
```bash
python3 Notifications/admin_alert.py
```

do similar for send_client_alert(test_alert)
---

*Built by Parin*