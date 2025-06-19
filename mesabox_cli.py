from mesabox.core import *
from mesabox.scanner import scan_network, scan_ports, parse_ports
from mesabox.wifi import scan_bssid, load_bssid_list, deauth_attack, select_bssid_from_list, BSSID_JSON_PATH
from mesabox.flood import udp_flood, tcp_flood
from mesabox.tools import ping_ip, show_network_interfaces
import os

def main():
    while True:
        print("\n=== MesaBox Menu ===")
        print("1. UDP Flood")
        print("2. TCP Flood")
        print("3. Ping an IP")
        print("4. Scan local network")
        print("5. Scan Wi-Fi BSSID/SSID")
        print("6. Wi-Fi Deauth Attack")
        print("7. Clear saved BSSID/SSID list")
        print("8. Show network interfaces")
        print("9. Scan ports of an IP")
        print("0. Quit")
        choice = input("Choice: ").strip()
        print(f"[INFO] Selected option: {choice}")

        if choice == "1":
            require_root()
            if not confirm_action("Are you sure you want to launch a UDP flood attack?"):
                print("Action cancelled.")
                continue
            target_ip = input("Target IP: ").strip()
            if not is_valid_ip(target_ip):
                print("[ERROR] Invalid IP address.")
                continue
            target_port = get_int("Target port [80]: ", 80)
            duration = get_int("Duration in seconds [10]: ", 10)
            pps = get_int("Packets per second [10]: ", 10)
            threads = get_int("Number of threads [1]: ", 1)
            weight = get_int("Request weight (1-10) [1]: ", 1)
            udp_flood(target_ip, target_port, duration, pps, threads, weight)
        elif choice == "2":
            require_root()
            if not confirm_action("Are you sure you want to launch a TCP flood attack?"):
                print("Action cancelled.")
                continue
            target_ip = input("Target IP: ").strip()
            if not is_valid_ip(target_ip):
                print("[ERROR] Invalid IP address.")
                continue
            target_port = get_int("Target port [80]: ", 80)
            duration = get_int("Duration in seconds [10]: ", 10)
            pps = get_int("Packets per second [10]: ", 10)
            threads = get_int("Number of threads [1]: ", 1)
            weight = get_int("Request weight (1-10) [1]: ", 1)
            tcp_flood(target_ip, target_port, duration, pps, threads, weight)
        elif choice == "3":
            ip = input("IP to ping: ").strip()
            if not is_valid_ip(ip):
                print("[ERROR] Invalid IP address.")
                continue
            ping_ip(ip)
        elif choice == "4":
            subnet = input("Enter local network prefix (e.g. 192.168.1): ").strip()
            if not subnet or not subnet.count('.') == 2:
                print("[ERROR] Invalid network prefix.")
                continue
            scan_network(subnet)
        elif choice == "5":
            require_root()
            iface = input("Wi-Fi interface name (e.g. wlan0): ").strip() or "wlan0"
            save = input("Save results to JSON file? (y/N): ").lower() == "y"
            scan_bssid(iface, save)
        elif choice == "6":
            require_root()
            if not confirm_action("Are you sure you want to launch a Wi-Fi deauth attack?"):
                print("Action cancelled.")
                continue
            print("1. Use a saved BSSID")
            print("2. Enter a custom BSSID")
            mode = input("Choice: ").strip()
            if mode == "1":
                bssid_list = load_bssid_list()
                bssid = select_bssid_from_list(bssid_list)
                if not bssid:
                    continue
            else:
                bssid = input("Access point BSSID: ").strip()
            client = input("Client MAC (leave blank for all): ").strip()
            if not client:
                client = "ff:ff:ff:ff:ff:ff"
            iface = input("Wi-Fi interface (e.g. wlan0mon): ").strip() or "wlan0mon"
            count = get_int("Number of packets [100]: ", 100)
            deauth_attack(bssid, client, iface, count)
        elif choice == "7":
            if not confirm_action("Are you sure you want to clear the saved BSSID/SSID list?"):
                print("Action cancelled.")
                continue
            if os.path.exists(BSSID_JSON_PATH):
                os.remove(BSSID_JSON_PATH)
                print("BSSID/SSID list cleared.")
            else:
                print("No list to clear.")
        elif choice == "8":
            show_network_interfaces()
        elif choice == "9":
            ip = input("IP to scan: ").strip()
            if not is_valid_ip(ip):
                print("[ERROR] Invalid IP address.")
                continue
            ports_input = input("Ports to scan (e.g. 22,80,443 or 20-25 or blank for 1-1000): ").strip()
            if ports_input:
                ports = parse_ports(ports_input)
                if not ports:
                    print("[ERROR] No valid ports provided.")
                    continue
            else:
                ports = None
            scan_ports(ip, ports)
        elif choice == "0":
            print("[INFO] Exiting program.")
            break
        else:
            print("[ERROR] Invalid choice.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[FATAL] An unexpected error occurred: {e}")
