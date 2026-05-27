import threading
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from LogHound.failed_logins import detect_failed_logins
from LogHound.new_ip import new_ip_login
from LogHound.new_location import new_location_login
from IntegrityX.file_monitor import OnMyWatch
from Notifications.admin_alert import send_admin_alert
from Notifications.client_alert import send_client_alert
from Dashboard.app import app

# ─────────────────────────────────────────
# LOGHOUND — runs every 60 seconds
# ─────────────────────────────────────────
def run_loghound():
    print("🐕 LogHound started...")
    alerts = []
    alerts += detect_failed_logins()
    alerts += new_ip_login()
    alerts += new_location_login()

    for alert in alerts:
        send_admin_alert(alert)
        if alert.get('severity') in ['HIGH', 'CRITICAL'] or alert['type'] in ['NEW_IP', 'NEW_LOCATION']:
            send_client_alert(alert)

    print(f"🐕 LogHound found {len(alerts)} alerts")

# ─────────────────────────────────────────
# INTEGRITYX — runs continuously
# ─────────────────────────────────────────
def run_integrityx():
    print("📁 IntegrityX started...")
    watch = OnMyWatch()
    alerts = watch.run()

    for alert in alerts:
        send_admin_alert(alert)
        send_client_alert(alert)

    print(f"📁 IntegrityX found {len(alerts)} alerts")

# ─────────────────────────────────────────
# DASHBOARD — runs Flask
# ─────────────────────────────────────────
def run_dashboard():
    print("📊 Dashboard started at http://localhost:5000")
    app.run(debug=False, port=5000)

# ─────────────────────────────────────────
# MAIN — starts all 3 threads
# ─────────────────────────────────────────
if __name__ == '__main__':
    print("""
    ██╗   ██╗██╗ ██████╗ ██╗██╗      █████╗ ███╗   ██╗████████╗██╗  ██╗
    ██║   ██║██║██╔════╝ ██║██║     ██╔══██╗████╗  ██║╚══██╔══╝╚██╗██╔╝
    ██║   ██║██║██║  ███╗██║██║     ███████║██╔██╗ ██║   ██║    ╚███╔╝ 
    ╚██╗ ██╔╝██║██║   ██║██║██║     ██╔══██║██║╚██╗██║   ██║    ██╔██╗ 
     ╚████╔╝ ██║╚██████╔╝██║███████╗██║  ██║██║ ╚████║   ██║   ██╔╝ ██╗
      ╚═══╝  ╚═╝ ╚═════╝ ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝
    """)
    print("🛡️  VigilantX Security Monitoring System")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    t1 = threading.Thread(target=run_loghound,   daemon=True)
    t2 = threading.Thread(target=run_integrityx, daemon=True)
    t3 = threading.Thread(target=run_dashboard,  daemon=True)

    t1.start()
    t2.start()
    t3.start()

    # Keep main thread alive
    while True:
        time.sleep(1)