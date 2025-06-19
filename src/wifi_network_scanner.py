import subprocess
import re
import shutil
import socket

def scan_wifi_networks(interface="wlan0"):
    """
    Scanne les réseaux Wi-Fi à proximité et affiche BSSID (MAC) et SSID.
    Utilise 'iwlist' ou 'iw' selon disponibilité.
    """
    networks = []
    if shutil.which("iwlist"):
        try:
            output = subprocess.check_output(
                ["sudo", "iwlist", interface, "scan"],
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            cells = re.split(r'Cell \d+ - ', output)[1:]
            for cell in cells:
                bssid_match = re.search(r'Address: ([0-9A-Fa-f:]{17})', cell)
                ssid_match = re.search(r'ESSID:"(.*?)"', cell)
                if bssid_match:
                    bssid = bssid_match.group(1)
                    ssid = ssid_match.group(1) if ssid_match else ""
                    ssid = ssid.replace('\x00', '').strip()
                    networks.append({'bssid': bssid, 'ssid': ssid})
        except Exception as e:
            print(f"Erreur lors du scan avec iwlist : {e}")
            return []
    elif shutil.which("iw"):
        try:
            output = subprocess.check_output(
                ["sudo", "iw", "dev", interface, "scan"],
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            current_bssid = None
            current_ssid = ""
            for line in output.splitlines():
                line = line.strip()
                if line.startswith("BSS "):
                    if current_bssid:
                        networks.append({'bssid': current_bssid, 'ssid': current_ssid})
                    current_bssid = line.split()[1].split('(')[0].strip()[:17]
                    current_ssid = ""
                elif line.startswith("SSID:"):
                    current_ssid = line[5:].strip()
            if current_bssid:
                networks.append({'bssid': current_bssid, 'ssid': current_ssid})
        except Exception as e:
            print(f"Erreur lors du scan avec iw : {e}")
            return []
    else:
        print("Erreur : ni 'iwlist' ni 'iw' ne sont installés ou trouvés dans le PATH.")
        return []

    print("Réseaux Wi-Fi détectés :")
    for net in networks:
        print(f"BSSID: {net['bssid']} | SSID: {net['ssid']}")
    return networks

def get_ip_from_bssid(bssid, interface="wlan0"):
    """
    Tente de déterminer l'IP d'un point d'accès Wi-Fi à partir de son BSSID.
    Cela n'est généralement pas possible directement, mais on peut scanner le réseau local.
    """
    # Cette fonction est un placeholder, car il n'existe pas de correspondance directe fiable.
    # On peut cependant scanner le réseau local pour trouver les IP actives.
    return None

def scan_wifi_ips(interface="wlan0", prefix=None):
    """
    Scanne le réseau local pour trouver les IP actives (clients et points d'accès).
    """
    print(f"[INFO] Début du scan IP sur {interface}")
    if prefix:
        subnet = prefix
        print(f"[INFO] Utilisation du préfixe fourni : {subnet}.0/24")
    else:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            print(f"[INFO] IP locale détectée : {local_ip}")
            subnet = ".".join(local_ip.split(".")[:3])
        except Exception:
            print("[ERREUR] Impossible de déterminer l'IP locale.")
            return []

    print(f"[INFO] Scan du réseau {subnet}.0/24 ...")
    active_ips = []
    total = 254
    for i in range(1, 255):
        ip = f"{subnet}.{i}"
        print(f"[SCAN] Test de {ip} ({i}/{total})", end='\r')
        try:
            res = subprocess.call(
                ["ping", "-c", "1", "-W", "1", ip],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            if res == 0:
                print(f"[OK] IP active trouvée : {ip}")
                active_ips.append(ip)
        except Exception:
            print(f"[ERREUR] Echec du ping pour {ip}")
            continue

    print("\n[INFO] Scan terminé.")
    print("[RESULTAT] IP actives détectées :")
    for ip in active_ips:
        print(ip)
    return active_ips

def scan_external_ips(prefix):
    """
    Scan an external network like x.y.z.0/24 (e.g. 8.8.8.0/24) for active IPs.
    """
    print(f"[INFO] Scanning external network {prefix}.0/24 ...")
    active_ips = []
    total = 254
    for i in range(1, 255):
        ip = f"{prefix}.{i}"
        print(f"[SCAN] Testing {ip} ({i}/{total})", end='\r')
        try:
            res = subprocess.call(
                ["ping", "-c", "1", "-W", "1", ip],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            if res == 0:
                print(f"[OK] Active IP found: {ip}")
                active_ips.append(ip)
        except Exception:
            print(f"[ERROR] Ping failed for {ip}")
            continue

    print("\n[INFO] Scan finished.")
    print("[RESULT] Active IPs found:")
    for ip in active_ips:
        print(ip)
    return active_ips

if __name__ == "__main__":
    prefix = input("External network prefix to scan (e.g. 8.8.8): ").strip()
    if prefix:
        scan_external_ips(prefix)
    else:
        print("[ERROR] No prefix provided.")
