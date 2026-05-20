# VigilantX - LogHound
# generate_logs.py
# This script generates fake login logs to test LogHound

import random
from datetime import datetime, timedelta


users = ["admin", "john", "sarah", "root", "client1"]


known_ips = {
    "192.168.1.10": "India",
    "192.168.1.11": "India",
    "192.168.1.12": "India",
}

unknown_ips = {
    "45.33.32.156" : "Russia",
    "203.45.67.89" : "China",
    "185.220.101.1": "USA",
    "99.99.99.99"  : "Brazil",
}

def generate_logs(num_lines=100):
    logs = []
    base_time = datetime.now()

    # Generate random normal logs
    for i in range(num_lines):
        time     = base_time + timedelta(minutes=i)
        user     = random.choice(users)
        ip       = random.choice(list(known_ips.keys()))  # mostly known IPs
        location = known_ips[ip]
        status   = random.choice(["SUCCESS", "FAILED", "FAILED"])

        log_line = (
            f"{time.strftime('%Y-%m-%d %H:%M:%S')} | "
            f"USER: {user} | "
            f"STATUS: {status} | "
            f"IP: {ip} | "
            f"LOCATION: {location}"
        )
        logs.append(log_line)

    # ── Scenario 1: Brute Force Attack ──
    # 15 failed logins in a row from Russia
    brute_time = base_time + timedelta(hours=2)
    for i in range(15):
        t = brute_time + timedelta(seconds=i)
        logs.append(
            f"{t.strftime('%Y-%m-%d %H:%M:%S')} | "
            f"USER: admin | "
            f"STATUS: FAILED | "
            f"IP: 45.33.32.156 | "
            f"LOCATION: Russia"
        )

    # ── Scenario 2: New IP Login ──
    # Someone logs in from a brand new IP never seen before
    new_ip_time = base_time + timedelta(hours=3)
    logs.append(
        f"{new_ip_time.strftime('%Y-%m-%d %H:%M:%S')} | "
        f"USER: john | "
        f"STATUS: SUCCESS | "
        f"IP: 99.99.99.99 | "
        f"LOCATION: Brazil"
    )

    # ── Scenario 3: New Location Login ──
    # Known IP but logging in from a new country
    new_loc_time = base_time + timedelta(hours=4)
    logs.append(
        f"{new_loc_time.strftime('%Y-%m-%d %H:%M:%S')} | "
        f"USER: sarah | "
        f"STATUS: SUCCESS | "
        f"IP: 203.45.67.89 | "
        f"LOCATION: China"
    )

    # Write all logs to file
    with open("logs/auth.log", "w") as f:
        f.write("\n".join(logs))

    print(f"✅ Generated {len(logs)} log lines → saved to logs/auth.log")
    print(f"   Scenarios included:")
    print(f"   🔴 Brute force attack (15 failed logins from Russia)")
    print(f"   🆕 New IP login (Brazil - 99.99.99.99)")
    print(f"   🌍 New location login (China - sarah)")


if __name__ == "__main__":
    generate_logs()