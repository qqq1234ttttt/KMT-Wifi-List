import nmap

def ping_scan(ip_range):
    nm = nmap.PortScanner()
    print(f"\n[+] Scanning network: {ip_range}\n")

    nm.scan(hosts=ip_range, arguments='-sn')

    for host in nm.all_hosts():
        print("=================================")
        print(f"IP: {host}")
        print(f"State: {nm[host].state()}")

        try:
            mac = nm[host]['addresses'].get('mac', 'Unknown')
            print(f"MAC: {mac}")
        except:
            print("MAC: Unknown")

    print("=================================")


def port_scan(target):
    nm = nmap.PortScanner()
    print(f"\n[+] Scanning ports on: {target}\n")

    nm.scan(target, arguments='-F')  # Fast scan (top ports)

    for host in nm.all_hosts():
        print("=================================")
        print(f"Host: {host}")

        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            for port in ports:
                state = nm[host][proto][port]['state']
                print(f"Port {port}: {state}")

    print("=================================")


def main():
    while True:
        print("\n==== Network Tool Menu ====")
        print("1. Scan network (devices)")
        print("2. Scan ports (single IP)")
        print("3. Exit")

        choice = input("Select option: ")

        if choice == "1":
            ip_range = input("Enter IP range (e.g. 192.168.100.0/24): ")
            ping_scan(ip_range)

        elif choice == "2":
            target = input("Enter target IP (e.g. 192.168.100.1): ")
            port_scan(target)

        elif choice == "3":
            print("Bye 👋")
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
