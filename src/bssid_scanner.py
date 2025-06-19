import subprocess
import re
import json
import os
import shutil

BSSID_JSON_PATH = "/home/thomas/pentest/bssid_list.json"

def scan_bssid(interface="wlan0", save=False):
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
        print("On Linux, install with:")
        print("  sudo apt install wireless-tools   # Debian/Ubuntu")
        print("  sudo pacman -S wireless_tools     # Arch/Manjaro")
        print("  sudo dnf install iw               # Fedora/RHEL")
        print("  sudo zypper install wireless-tools # openSUSE")
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

if __name__ == "__main__":
    iface = input("Wi-Fi interface name (e.g. wlan0): ") or "wlan0"
    action = input("Do you want to scan (s) or load from file (l)? ")
    if action.lower() == 's':
        save_option = input("Do you want to save the result to a JSON file? (y/n) ")
        scan_bssid(iface, save=(save_option.lower() == 'y'))
    elif action.lower() == 'l':
        load_bssid_list()
    else:
        print("Unrecognized action.")
