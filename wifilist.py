import nmap
import subprocess
import ipaddress
import re
import os
import time

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
        ⚡ K M T STABLE v2 ⚡
""")

# =========================
# 🌐 SAFE IP DETECT (FIXED)
# =========================
def get_ip_range():
    cmd = "ip route | grep src"
    out = subprocess.getoutput(cmd)

    match = re.search(r"src (\d+\.\d+\.\d+\.\d+)", out)

    if not match:
        print("[-] Cannot detect real WiFi IP!")
        print(out)
        exit()

    ip = match.group(1)

    # ❌ block loopback / invalid
    if ip.startswith("127.") or ip.startswith("169.254"):
        print("[-] Invalid network detected (loopback/APIPA)")
        exit()

    print(f"[+] Real WiFi IP: {ip}")

    net = ipaddress.IPv4Interface(ip + "/24").network
    return str(net)

# =========================
# 🔍 SCAN (FILTERED)
# =========================
def scan_network(ip_range):
    nm = nmap.PortScanner()

    print(f"\n[+] Scanning: {ip_range}\n")

    nm.scan(hosts=ip_range, arguments='-sn')

    for host in nm.all_hosts():

        # ❌ skip fake localhost
        if host.startswith("127."):
            continue

        state = nm[host].state()
        mac = nm[host]['addresses'].get('mac', 'Unknown')

        print("=================================")
        print(f"IP   : {host}")
        print(f"State: {state}")
        print(f"MAC  : {mac}")

    print("=================================")

# =========================
# 🚀 RUN
# =========================
def main():
    os.system("clear")
    logo()

    ip_range = get_ip_range()
    scan_network(ip_range)

if __name__ == "__main__":
    main()
