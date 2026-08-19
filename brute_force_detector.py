#!/usr/bin/env python3
"""
SSH Brute Force Detector
Analyzes authentication logs to identify IP addresses conducting
SSH brute force attacks based on failed login frequency.

Usage: python3 brute_force_detector.py <logfile> [threshold]
Example: python3 brute_force_detector.py /var/log/auth.log 5

Author: Tyrik Parker
"""

import re
import sys
from collections import Counter


def parse_log(logfile):
    """Read a log file and return a list of attacker IPs from failed logins."""
    attacker_ips = []

    try:
        with open(logfile, "r") as file:
            for line in file:
                if "Failed password" in line:
                    match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
                    if match:
                        attacker_ips.append(match.group(1))
    except FileNotFoundError:
        print(f"[ERROR] Log file not found: {logfile}")
        sys.exit(1)

    return attacker_ips


def detect_attackers(attacker_ips, threshold):
    """Count IPs and print a report flagging those above the threshold."""
    ip_counts = Counter(attacker_ips)

    print("\n=== SSH BRUTE FORCE DETECTION REPORT ===")
    print(f"Total failed login attempts: {len(attacker_ips)}")
    print(f"Unique source IPs: {len(ip_counts)}")
    print(f"Alert threshold: {threshold} failed attempts\n")

    alerts = 0
    for ip, count in ip_counts.most_common():
        if count >= threshold:
            print(f"[!] ALERT: {ip} - {count} failed attempts - LIKELY ATTACKER")
            alerts += 1
        else:
            print(f"[ ] {ip} - {count} failed attempts")

    print(f"\nSummary: {alerts} IP(s) flagged as likely attackers.\n")


def main():
    # Require at least a logfile argument
    if len(sys.argv) < 2:
        print("Usage: python3 brute_force_detector.py <logfile> [threshold]")
        sys.exit(1)

    logfile = sys.argv[1]
    # Use provided threshold, or default to 5
    threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    attacker_ips = parse_log(logfile)
    detect_attackers(attacker_ips, threshold)


if __name__ == "__main__":
    main()
