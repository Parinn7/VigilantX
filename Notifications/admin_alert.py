import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

def send_admin_alert(alert):
    load_dotenv()
    sender_email    = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    admin_email     = os.getenv("ADMIN_EMAIL")

    # ── Subject ──
    if alert['type'] == 'BRUTE_FORCE':
        subject = " VigilantX: Brute Force Attack Detected"
    elif alert['type'] == 'NEW_IP':
        subject = " VigilantX: New Login IP Detected"
    elif alert['type'] == 'NEW_LOCATION':
        subject = " VigilantX: New Login Location Detected"
    elif alert['type'] == 'RANSOMWARE':
        subject = " VigilantX: RANSOMWARE Activity Detected"
    elif alert['type'] == 'CREATED':
        subject = " VigilantX: New File Created"
    elif alert['type'] == 'MODIFIED':
        subject = " VigilantX: File Modified"
    elif alert['type'] == 'DELETED':
        subject = " VigilantX: File Deleted"
    elif alert['type'] == 'RENAME':
        subject = " VigilantX: File Renamed"
    else:
        subject = "VigilantX: Security Alert"

    # ── Body ──
    if alert['type'] == 'BRUTE_FORCE':
        body = f"""
VigilantX Security Alert — ADMIN REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Attack Type : Brute Force
User        : {alert['user']}
IP          : {alert['ip']}
Location    : {alert['location']}
Attempts    : {alert['count']}
Severity    : {alert['severity']}
Time        : {alert['time']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Action Required: Block IP immediately.
        """

    elif alert['type'] == 'NEW_IP':
        body = f"""
VigilantX Security Alert — ADMIN REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Alert Type  : New IP Login
User        : {alert['user']}
New IP      : {alert['ip']}
Location    : {alert['location']}
Time        : {alert['time']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Action Required: Verify if this login was legitimate.
        """

    elif alert['type'] == 'NEW_LOCATION':
        body = f"""
VigilantX Security Alert — ADMIN REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Alert Type  : New Location Login
User        : {alert['user']}
Location    : {alert['Location']}
IP          : {alert['IP']}
Time        : {alert['time']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Action Required: Verify if this login was legitimate.
        """

    elif alert['type'] == 'RANSOMWARE':
        body = f"""
VigilantX Security Alert — ADMIN REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Alert Type      : RANSOMWARE DETECTED
Files Affected  : {alert['count']}
Started At      : {alert['start_time']}
Files List      : {', '.join(alert['file_affected'])}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Action Required: SHUT DOWN SYSTEM IMMEDIATELY.
        """

    elif alert['type'] in ['CREATED', 'MODIFIED', 'DELETED', 'RENAME']:
        body = f"""
VigilantX Security Alert — ADMIN REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Alert Type  : File {alert['type']}
File        : {alert['filename']}
Time        : {alert['timestamp']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Action Required: Review file activity.
        """

    else:
        body = f"VigilantX Security Alert: {alert}"

    # ── Send Email ──
    msg = MIMEMultipart()
    msg['From']    = sender_email
    msg['To']      = admin_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, admin_email, msg.as_string())
        server.quit()
        print(f" Admin alert sent: {subject}")
    except Exception as e:
        print(f" Failed to send admin alert: {e}")

