PRELOADED_LOC = {"India"}

def new_location_login():

    location_logins = {}
    alerts = []

    with open("logs/auth.log", "r") as f:
        lines = f.readlines()
    for line in lines:
        parts = line.strip().split("|")
        if "SUCCESS" in line:
            user = parts[1].replace("USER:", "").strip()
            loc = parts[4].replace("LOCATION:","").strip()

            if user not in location_logins:
                location_logins[user] = PRELOADED_LOC.copy()
            
            if loc not in location_logins[user]:
                alert = {
                    "type": "NEW_LOCATION",
                    "user" : user,
                    "Location" : loc,
                    "time" : parts[0].strip(),
                    "reason" : "New login location detected for user",
                    "IP" : parts[3].replace("IP:","").strip()
                }
                location_logins[user].add(loc)
                alerts.append(alert)
    return alerts

if __name__ == "__main__":
    alerts = new_location_login()
    
    print(f"\n LogHound - New Location Detection")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Total alerts found: {len(alerts)}\n")
    
    for alert in alerts:
        print(f" New Location Detected!")
        print(f"   User     : {alert['user']}")
        print(f"   Location : {alert['Location']}")
        print(f"   IP       : {alert['IP']}")
        print(f"   Time     : {alert['time']}")
        print(f"Reason    : {alert['reason']}")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")