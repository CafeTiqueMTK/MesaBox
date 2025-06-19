import sys
import os

def get_int(prompt, default):
    try:
        return int(input(prompt) or default)
    except ValueError:
        print("Entrée invalide, valeur par défaut utilisée.")
        return default

def main():
    print("=== MesaBox Menu ===")
    print("1. UDP Flood")
    print("2. TCP Flood")
    print("3. Ping an IP")
    print("4. Scan local network")
    print("5. Scan Wi-Fi BSSID/SSID")
    print("6. Wi-Fi Deauth Attack")
    print("7. Clear saved BSSID/SSID list")
    print("8. Show network interfaces")
    print("9. Scan external network IPs (by prefix)")
    print("10. Scan ports of an IP")
    print("0. Quit")
    choice = input("Choice: ")
    print(f"[INFO] Selected option: {choice}")

    if choice == "1":
        print("[INFO] UDP Flood option selected.")
        from src.udp_flood import udp_flood
        target_ip = input("Target IP: ")
        target_port = get_int("Target port [80]: ", 80)
        duration = get_int("Duration in seconds [10]: ", 10)
        pps = get_int("Packets per second [10]: ", 10)
        threads = get_int("Number of threads [1]: ", 1)
        weight = get_int("Request weight (1-10) [1]: ", 1)
        udp_flood(target_ip, target_port, duration, pps, threads, weight)
        sys.exit(0)
    elif choice == "2":
        print("[INFO] TCP Flood option selected.")
        from src.tcp_flood import tcp_flood
        target_ip = input("Target IP: ")
        target_port = get_int("Target port [80]: ", 80)
        duration = get_int("Duration in seconds [10]: ", 10)
        pps = get_int("Packets per second [10]: ", 10)
        threads = get_int("Number of threads [1]: ", 1)
        weight = get_int("Request weight (1-10) [1]: ", 1)
        tcp_flood(target_ip, target_port, duration, pps, threads, weight)
        sys.exit(0)
    elif choice == "3":
        print("[INFO] Ping option selected.")
        from src import ping_ip
        ip = input("IP to ping: ")
        ping_ip(ip)
        sys.exit(0)
    elif choice == "4":
        print("[INFO] Local network scan option selected.")
        from src import scan_network
        subnet = input("Enter local network prefix (e.g. 192.168.1): ")
        print("Scanning...")
        active_ips = scan_network(subnet)
        print("Active IPs detected:")
        for ip in active_ips:
            print(ip)
        sys.exit(0)
    elif choice == "5":
        print("[INFO] Wi-Fi BSSID/SSID scan option selected.")
        from src import scan_bssid
        iface = input("Wi-Fi interface name (e.g. wlan0): ") or "wlan0"
        save = input("Save results to JSON file? (y/N): ").lower() == "y"
        scan_bssid(iface, save)
        sys.exit(0)
    elif choice == "6":
        print("[INFO] Deauth Attack option selected.")
        from src import deauth_attack, load_bssid_list
        from src.deauth_attack import select_bssid_from_list
        print("1. Use a saved BSSID")
        print("2. Enter a custom BSSID")
        mode = input("Choice: ")
        if mode == "1":
            bssid_list = load_bssid_list()
            bssid = select_bssid_from_list(bssid_list)
            if not bssid:
                sys.exit(0)
        else:
            bssid = input("Access point BSSID: ")
        client = input("Client MAC (leave blank for all): ")
        if not client.strip():
            client = "ff:ff:ff:ff:ff:ff"
        iface = input("Wi-Fi interface (e.g. wlan0mon): ") or "wlan0mon"
        count = input("Number of packets [100]: ") or "100"
        deauth_attack(bssid, client, iface, int(count))
        sys.exit(0)
    elif choice == "7":
        print("[INFO] Clear BSSID/SSID list option selected.")
        import os
        from src.bssid_scanner import BSSID_JSON_PATH
        if os.path.exists(BSSID_JSON_PATH):
            os.remove(BSSID_JSON_PATH)
            print("BSSID/SSID list cleared.")
        else:
            print("No list to clear.")
        sys.exit(0)
    elif choice == "8":
        print("[INFO] Show network interfaces option selected.")
        from src.network_info import show_network_interfaces
        show_network_interfaces()
        sys.exit(0)
    elif choice == "9":
        print("[INFO] External network IP scan option selected.")
        from src.wifi_network_scanner import scan_external_ips
        prefix = input("External network prefix to scan (e.g. 8.8.8): ").strip()
        if prefix:
            scan_external_ips(prefix)
        else:
            print("[ERROR] No prefix provided.")
        sys.exit(0)
    elif choice == "10":
        print("[INFO] Port scan option selected.")
        from src.port_scanner import scan_ports
        ip = input("IP to scan: ")
        ports_input = input("Ports to scan (e.g. 22,80,443 or blank for 1-1000): ")
        if ports_input.strip():
            ports = [int(p.strip()) for p in ports_input.split(",") if p.strip().isdigit()]
        else:
            ports = None
        scan_ports(ip, ports)
        sys.exit(0)
    elif choice == "0":
        print("[INFO] Exiting program.")
        sys.exit(0)
    else:
        print("[ERROR] Invalid choice.")
        sys.exit(1)

    target_ip = input("IP cible: ")
    target_port = get_int("Port cible [80]: ", 80)
    duration = get_int("Durée en secondes [10]: ", 10)
    pps = get_int("Cadence (paquets/sec) [10]: ", 10)
    threads = get_int("Nombre de threads [1]: ", 1)

    if choice == "1":
        print("[INFO] Option UDP Flood sélectionnée.")
        from src.udp_flood import udp_flood
        udp_flood(target_ip, target_port, duration, pps, threads)
    elif choice == "2":
        print("[INFO] Option TCP Flood sélectionnée.")
        from src.tcp_flood import tcp_flood
        tcp_flood(target_ip, target_port, duration, pps, threads)

    print("Attaque terminée. Consultez les fichiers de logs.")

if __name__ == "__main__":
    main()
