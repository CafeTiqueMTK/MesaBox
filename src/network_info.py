import platform
import subprocess

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

if __name__ == "__main__":
    show_network_interfaces()
    show_network_interfaces()
