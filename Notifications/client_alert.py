import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

def send_client_alert(alert):
    load_dotenv()
    sender_email    = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    client_email    = os.getenv("CLIENT_EMAIL")

    # ── Subject ──
    if alert['type'] == 'BRUTE_FORCE':
        subject = " Security Alert: Suspicious Login Activity"
    elif alert['type'] == 'NEW_IP':
        subject = " Security Alert: New Device Login Detected"
    elif alert['type'] == 'NEW_LOCATION':
        subject = " Security Alert: New Location Login Detected"
    elif alert['type'] == 'RANSOMWARE':
        subject = " CRITICAL: Mass File Tampering Detected"
    elif alert['type'] in ['CREATED', 'MODIFIED', 'DELETED', 'RENAME']:
        subject = "📁 Security Alert: File Activity Detected"
    else:
        subject = "Security Alert from VigilantX"

    # ── Body — Simple plain English ──
    if alert['type'] == 'BRUTE_FORCE':
        body = f"""
Dear Client,

We detected multiple failed login attempts on your system.

Someone tried to login {alert['count']} times unsuccessfully.
Our security team has been notified and is investigating.

Time: {alert['time']}

Your security is our priority.
— VigilantX Security Team
        """

    elif alert['type'] == 'NEW_IP':
        body = f"""
Dear Client,

A login was detected from a new device on your account.

User     : {alert['user']}
Location : {alert['location']}
Time     : {alert['time']}

If this was you, no action needed.
If this was NOT you, please contact us immediately.

— VigilantX Security Team
        """

    elif alert['type'] == 'NEW_LOCATION':
        body = f"""
Dear Client,

A login was detected from a new location on your account.

User     : {alert['user']}
Location : {alert['Location']}
Time     : {alert['time']}

If this was you, no action needed.
If this was NOT you, please contact us immediately.

— VigilantX Security Team
        """

    elif alert['type'] == 'RANSOMWARE':
        body = f"""
Dear Client,

CRITICAL ALERT: Unusual mass file activity was detected on your system.

Files affected : {alert['count']}
Time           : {alert['start_time']}

Our security team has been notified and is responding immediately.
Please do not access your system until further notice.

— VigilantX Security Team
        """

    elif alert['type'] in ['CREATED', 'MODIFIED', 'DELETED', 'RENAME']:
        body = f"""
Dear Client,

A file on your system was {alert['type'].lower()}.

File : {alert['filename']}
Time : {alert['timestamp']}

Our security team has been notified.

— VigilantX Security Team
        """

    else:
        body = "A security event was detected on your system. Our team is investigating."

    # ── Send Email ──
    msg = MIMEMultipart()
    msg['From']    = sender_email
    msg['To']      = client_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, client_email, msg.as_string())
        server.quit()
        print(f" Client alert sent: {subject}")
    except Exception as e:
        print(f" Failed to send client alert: {e}")

