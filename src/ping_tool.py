import os
import platform

def ping_ip(ip):
    print(f"[INFO] Starting ping to {ip} ...")
    param = "-n" if platform.system().lower() == "windows" else "-c"
    response = os.system(f"ping {param} 4 {ip}")
    if response == 0:
        print(f"[OK] {ip} is reachable.")
    else:
        print(f"[ERROR] {ip} is not reachable.")
    print("[INFO] Ping finished.")
