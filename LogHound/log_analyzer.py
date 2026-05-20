from failed_logins import detect_failed_logins
from new_location import new_location_login
from new_ip import new_ip_login

if __name__ == "__main__":
    print(f"\n🐕 LogHound - Security Alert Summary")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    failed_alerts = detect_failed_logins()
    ip_alerts = new_ip_login()
    loc_alerts = new_location_login()

    print(f"\n🔴 Failed Login Attempts: {len(failed_alerts)} alerts")
    for alert in failed_alerts:
        print(f"   🚨 {alert['severity']} alert for user '{alert['user']}' from IP {alert['ip']} at {alert['time']}")
        print(f"      Reason: {alert['Reason']}")

    print(f"\n🆕 New IP Logins: {len(ip_alerts)} alerts")
    for alert in ip_alerts:
        print(f"   🚨 New IP '{alert['ip']}' detected for user '{alert['user']}' at {alert['time']} from location {alert['location']}")

    print(f"\n🌍 New Location Logins: {len(loc_alerts)} alerts")
    for alert in loc_alerts:
        print(f"   🚨 New location '{alert['Location']}' detected for user '{alert['user']}' at {alert['time']} from IP {alert['IP']}") 
