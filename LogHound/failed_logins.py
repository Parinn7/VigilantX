from datetime import datetime, timedelta

MEDIUM_THRESHOLD = 10
HIGH_THRESHOLD = 20
EXTREME_THRESHOLD = 50
ALERT_COOL_DOWN = timedelta(minutes=10)

TIME_WINDOW = timedelta(minutes=5)

def detect_failed_logins():
    failed_attempts = {}
    alerts = []
    alert_set = {}

    with open("logs/auth.log","r") as f:
        lines = f.readlines()
    for line in lines:
        if "FAILED" in line:
            parts = line.strip().split("|")
            time_stamp = parts[0].strip()
            user = parts[1].replace("USER:","").strip()
            ip = parts[3].replace("IP:","").strip()
            loc = parts[4].replace("LOCATION:","").strip()
            time = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S")

            if user not in failed_attempts:
                failed_attempts[user] = []
            failed_attempts[user].append(time)

            window_start = time - TIME_WINDOW
            recent_attempts = [t for t in failed_attempts[user] if t >= window_start]
            count = len(recent_attempts)

            if count < MEDIUM_THRESHOLD:
                pass
            elif count < HIGH_THRESHOLD:
                severity = "MEDIUM"
            elif count < EXTREME_THRESHOLD:
                severity = "HIGH"
            else:
                severity = "CRITICAL"

            
            if count >= MEDIUM_THRESHOLD:
                if user not in alert_set or time - alert_set[user] > ALERT_COOL_DOWN:
                    alert_set[user] = time
                    alert = {
                        "type": "BruteForce",
                        "user": user,
                        "ip": ip,
                        "location": loc,
                        "count": count,
                        "severity": severity,
                        "time": time_stamp,
                        "Reason": f"{count} failed login attempts within {TIME_WINDOW.total_seconds()//60} minutes"
                    }
                    alerts.append(alert)

    return alerts


            
if __name__ == "__main__":
    alerts = detect_failed_logins()
    
    print(f"\n🐕 LogHound - Failed Login Detection")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Total alerts found: {len(alerts)}\n")
    
    for alert in alerts:
        print(f"🚨 Severity  : {alert['severity']}")
        print(f"   User      : {alert['user']}")
        print(f"   IP        : {alert['ip']}")
        print(f"   Location  : {alert['location']}")
        print(f"   Attempts  : {alert['count']}")
        print(f"   Time      : {alert['time']}")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")