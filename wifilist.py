import nmap
import subprocess
import ipaddress
import re
import os
import time
from datetime import datetime

KNOWN_DEVICES = set()

# =========================
# 🎨 LOGO
# =========================
def logo():
    print("""
██╗  ██╗     ███╗   ███╗     ████████╗
██║ ██╔╝     ████╗ ████║     ╚══██╔══╝
█████╔╝█████╗██╔████╔██║█████╗  ██║   
██╔═██╗╚════╝██║╚██╔╝██║╚════╝  ██║   
██║  ██╗     ██║ ╚═╝ ██║        ██║   
╚═╝  ╚═╝     ╚═╝     ╚═╝        ╚═╝   
   ⚡ K M T ULTIMATE PRO MONITOR ⚡
""")

# =========================
# 🌐 GET IP RANGE (ULTRA STABLE)
# =========================
def get_ip_range():
    cmds = ["ip route", "ifconfig", "ip a"]
    ip = None

    for c in cmds:
        out = subprocess.getoutput(c)

        match = re.search(r"src (\d+\.\d+\.\d+\.\d+)", out)
        if not match:
            match = re.search(r"inet (\d+\.\d+\.\d+\.\d+)", out)

        if match:
            ip = match.group(1)
            break

    if not ip:
        print("[-] Cannot detect IP!")
        exit()

    print(f"[+] Device IP: {ip}")

    net = ipaddress.IPv4Interface(ip + "/24").network
    return str(net)

# =========================
# 🔍 SCAN NETWORK
# =========================
def scan_network(ip_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, arguments='-sn')

    devices = []

    for host in nm.all_hosts():
        ip = host
        state = nm[host].state()
        mac = nm[host]['addresses'].get('mac', 'Unknown')

        devices.append((ip, mac))

    return devices

# =========================
# 🔔 ALERT SYSTEM
# =========================
def check_devices(devices):
    global KNOWN_DEVICES

    for ip, mac in devices:
        if mac != "Unknown" and mac not in KNOWN_DEVICES:
            print(f"\n⚠️ NEW DEVICE DETECTED: {ip} | {mac}")
            KNOWN_DEVICES.add(mac)

# =========================
# 💾 SAVE LOG
# =========================
def save_log(devices):
    with open("kmt_live_log.txt", "a") as f:
        f.write(f"\n=== {datetime.now()} ===\n")
        for ip, mac in devices:
            f.write(f"{ip} | {mac}\n")

# =========================
# 🔁 LIVE MONITOR
# =========================
def live_monitor():
    ip_range = get_ip_range()

    print("\n[+] Starting Live Monitor... (Ctrl+C to stop)\n")

    try:
        while True:
            devices = scan_network(ip_range)

            os.system("clear")
            logo()

            print(f"[LIVE SCAN] {datetime.now()}")
            print("=================================")

            for ip, mac in devices:
                print(f"IP: {ip} | MAC: {mac}")

            print("=================================")

            check_devices(devices)
            save_log(devices)

            time.sleep(5)

    except KeyboardInterrupt:
        print("\n[✓] Stopped Monitor")

# =========================
# 📋 MENU
# =========================
def menu():
    while True:
        print("\n====== K M T ULTIMATE PRO ======")
        print("1. Live Network Monitor")
        print("2. Exit")

        c = input("Select: ")

        if c == "1":
            live_monitor()

        elif c == "2":
            print("Bye 👋")
            break

        else:
            print("Invalid!")

# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    os.system("clear")
    logo()
    menu()
