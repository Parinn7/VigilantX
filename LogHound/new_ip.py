
PRELOADED_IPS = {"192.168.1.10", "192.168.1.11", "192.168.1.12"}

def new_ip_login():

    login_ips = {}
    alerts = []

    with open("logs/auth.log","r") as f:
        lines = f.readlines()
    for line in lines:
        if "SUCCESS" in line:
            parts = line.strip().split("|")
            ip = parts[3].replace("IP:","").strip()
            user = parts[1].replace("USER:","").strip()
            loc = parts[4].replace("LOCATION:","").strip()
            if user not in login_ips:
                login_ips[user] = PRELOADED_IPS.copy()  
            
            if ip not in login_ips[user]:
                alert = {
                "type": "NEW_IP",
                "user": user,
                "ip": ip,
                "time": parts[0].strip(),
                "reason": "New IP address detected for user",
                "location": loc
                }
                login_ips[user].add(ip)
                alerts.append(alert)
    return alerts


if __name__ == "__main__":
    alerts = new_ip_login()
    
    print(f"\n LogHound - New IP Detection")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Total alerts found: {len(alerts)}\n")
    
    for alert in alerts:
        print(f" New IP Detected!")
        print(f"   User     : {alert['user']}")
        print(f"   New IP   : {alert['ip']}")
        print(f"   Location : {alert['location']}")
        print(f"   Time     : {alert['time']}")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")