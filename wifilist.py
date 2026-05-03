import nmap
import subprocess
import ipaddress
import re
import time
import os

# =========================
# ✨ K M T TYPING LOGO
# =========================
def logo():
    text = """
██╗  ██╗     ███╗   ███╗     ████████╗
██║ ██╔╝     ████╗ ████║     ╚══██╔══╝
█████╔╝█████╗██╔████╔██║█████╗  ██║   
██╔═██╗╚════╝██║╚██╔╝██║╚════╝  ██║   
██║  ██╗     ██║ ╚═╝ ██║        ██║   
╚═╝  ╚═╝     ╚═╝     ╚═╝        ╚═╝   
        🛠 K M T NETWORK TOOL 🛠
"""
    for line in text.split("\n"):
        print(line)
        time.sleep(0.05)


# =========================
# 🌐 AUTO IP RANGE
# =========================
def get_ip_range():
    result = subprocess.getoutput("ip a show wlan0")
    ip_match = re.search(r"inet (\d+\.\d+\.\d+\.\d+)", result)

    if not ip_match:
        print("[-] Cannot detect IP!")
        exit()

    ip = ip_match.group(1)
    print(f"[+] Your IP: {ip}")

    network = ipaddress.IPv4Interface(ip + "/24").network
    return str(network)


# =========================
# 🔍 NETWORK SCAN
# =========================
def scan_network(ip_range):
    nm = nmap.PortScanner()
    print(f"\n[+] Scanning: {ip_range}\n")

    nm.scan(hosts=ip_range, arguments='-sn')

    results = []

    for host in nm.all_hosts():
        ip = host
        state = nm[host].state()
        mac = nm[host]['addresses'].get('mac', 'Unknown')

        print("=================================")
        print(f"IP   : {ip}")
        print(f"State: {state}")
        print(f"MAC  : {mac}")

        results.append(f"{ip} | {state} | {mac}")

    print("=================================")

    # save file
    with open("scan_result.txt", "w") as f:
        f.write("\n".join(results))

    print("\n[✓] Saved to scan_result.txt")


# =========================
# 📋 MENU
# =========================
def menu():
    while True:
        print("\n====== K M T PRO TOOL ======")
        print("1. Auto Network Scan")
        print("2. Exit")

        choice = input("Select: ")

        if choice == "1":
            ip_range = get_ip_range()
            scan_network(ip_range)

        elif choice == "2":
            print("Bye 👋")
            break

        else:
            print("Invalid option!")


# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    os.system("clear")
    logo()
    menu()
