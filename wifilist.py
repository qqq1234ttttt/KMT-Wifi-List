import nmap
import socket
import ipaddress
import time
import os
from datetime import datetime

KNOWN = set()

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
     ⚡ K M T FINAL ULTRA STABLE ⚡
""")

# =========================
# 🌐 SAFE IP DETECT (BEST METHOD)
# =========================
def get_ip_range():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()

        print(f"[+] Detected IP: {ip}")

        net = ".".join(ip.split(".")[:3]) + ".0/24"
        return net

    except:
        print("[-] IP detection failed!")
        exit()

# =========================
# 🔍 SCAN NETWORK
# =========================
def scan(ip_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, arguments='-sn')

    devices = []

    for host in nm.all_hosts():
        mac = nm[host]['addresses'].get('mac', 'Unknown')
        devices.append((host, mac))

    return devices

# =========================
# 🔔 ALERT SYSTEM
# =========================
def alert(devices):
    global KNOWN

    for ip, mac in devices:
        if mac != "Unknown" and mac not in KNOWN:
            print(f"\n⚠️ NEW DEVICE: {ip} | {mac}")
            KNOWN.add(mac)

# =========================
# 💾 LOG SAVE
# =========================
def save(devices):
    with open("kmt_final_log.txt", "a") as f:
        f.write(f"\n=== {datetime.now()} ===\n")
        for ip, mac in devices:
            f.write(f"{ip} | {mac}\n")

# =========================
# 🔁 LIVE MONITOR
# =========================
def live():
    ip_range = get_ip_range()

    print(f"[+] Monitoring: {ip_range}\n")

    try:
        while True:
            devices = scan(ip_range)

            os.system("clear")
            logo()

            print(f"[LIVE] {datetime.now()}")
            print("=================================")

            for ip, mac in devices:
                print(f"IP: {ip} | MAC: {mac}")

            print("=================================")

            alert(devices)
            save(devices)

            time.sleep(5)

    except KeyboardInterrupt:
        print("\n[✓] Stopped safely")

# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    os.system("clear")
    logo()
    live()
