import platform
import subprocess
import threading

def ping_ip_scan(ip, results):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", "-W", "1", ip] if platform.system().lower() != "windows" else ["ping", param, "1", ip]
    try:
        output = subprocess.DEVNULL
        result = subprocess.call(command, stdout=output, stderr=output)
        if result == 0:
            results.append(ip)
    except Exception:
        pass

def scan_network(base_ip, start=1, end=254, max_threads=100):
    print(f"[INFO] Starting network scan on {base_ip}.{start}-{end}")
    threads = []
    results = []
    for i in range(start, end + 1):
        ip = f"{base_ip}.{i}"
        print(f"[SCAN] Testing {ip} ...", end='\r')
        t = threading.Thread(target=ping_ip_scan, args=(ip, results))
        threads.append(t)
        t.start()
        if len(threads) >= max_threads:
            for t in threads:
                t.join()
            threads = []
    for t in threads:
        t.join()
    print("\n[INFO] Network scan finished.")
    return results

if __name__ == "__main__":
    subnet = input("Enter the local network prefix (e.g. 192.168.1): ")
    print("Scanning...")
    active_ips = scan_network(subnet)
    print("Active IPs detected:")
    for ip in active_ips:
        print(ip)
