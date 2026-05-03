import nmap
import socket
import ipaddress
import subprocess
import re
import os
import time
import requests
from datetime import datetime

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
   ⚡ K M T DEVICE MONITOR ⚡
""")

# =========================
# 🌐 GET IP (SAFE)
# =========================
def get_ip_range():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()

        print(f"[+] Your IP: {ip}")

        return ".".join(ip.split(".")[:3]) + ".0/24"

    except:
        print("[-] Cannot detect IP")
        exit()

# =========================
# 🧠 DEVICE NAME (VENDOR DETECT)
# =========================
def get_vendor(mac):
    try:
        if mac == "Unknown":
            return "Unknown Device"

        url = f"https://api.macvendors.com/{mac}"
        res = requests.get(url, timeout=3)

        if res.status_code == 200:
            return res.text
        else:
            return "Unknown Device"

    except:
        return "Unknown Device"

# =========================
# 🔍 SCAN NETWORK
# =========================
def scan_network(ip_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, arguments='-sn')

    devices = []

    for host in nm.all_hosts():
        if host.startswith("127."):
            continue

        mac = nm[host]['addresses'].get('mac', 'Unknown')
        vendor = get_vendor(mac)

        devices.append((host, mac, vendor))

    return devices

# =========================
# 📊 SHOW RESULTS
# =========================
def show(devices):
    os.system("clear")
    logo()

    print(f"[LIVE] {datetime.now()}")
    print("=================================")

    for ip, mac, vendor in devices:
        print(f"IP     : {ip}")
        print(f"MAC    : {mac}")
        print(f"Device : {vendor}")
        print("---------------------------------")

# =========================
# 🚀 RUN LOOP
# =========================
def main():
    os.system("clear")
    logo()

    ip_range = get_ip_range()

    print(f"[+] Scanning: {ip_range}\n")

    try:
        while True:
            devices = scan_network(ip_range)
            show(devices)
            time.sleep(5)

    except KeyboardInterrupt:
        print("\n[✓] Stopped safely")

# =========================
# START
# =========================
if __name__ == "__main__":
    main()
