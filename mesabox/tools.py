import os
import platform
import subprocess

def ping_ip(ip):
    print(f"[INFO] Starting ping to {ip} ...")
    if platform.system().lower() == "windows":
        param = "-n"
        wait = "-w 1000"
        cmd = f"ping {param} 4 {wait} {ip}"
    else:
        param = "-c"
        wait = "-W 1"
        cmd = f"ping {param} 4 {wait} {ip}"
    response = os.system(cmd)
    if response == 0:
        print(f"[OK] {ip} is reachable.")
    else:
        print(f"[ERROR] {ip} is not reachable.")
    print("[INFO] Ping finished.")

def show_network_interfaces():
    print("[INFO] Showing network interfaces...")
    system = platform.system().lower()
    if system == "linux":
        cmd = ["ip", "addr"]
    elif system == "windows":
        cmd = ["ipconfig", "/all"]
    elif system == "darwin":
        cmd = ["ifconfig"]
    else:
        print("[ERROR] Unsupported system.")
        return

    try:
        result = subprocess.check_output(cmd, universal_newlines=True)
        print(result)
        print("[INFO] Display finished.")
    except Exception as e:
        print(f"[ERROR] Getting network interfaces: {e}")
