import socket
import subprocess
import threading
import platform

def scan_network(base_ip, start=1, end=254, max_threads=100):
    print(f"[INFO] Starting network scan on {base_ip}.{start}-{end}")
    threads = []
    results = []
    def ping_ip_scan(ip, results):
        if platform.system().lower() == "windows":
            command = ["ping", "-n", "1", "-w", "1000", ip]
        else:
            command = ["ping", "-c", "1", "-W", "1", ip]
        try:
            output = subprocess.DEVNULL
            result = subprocess.call(command, stdout=output, stderr=output)
            if result == 0:
                results.append(ip)
        except Exception:
            pass
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

def parse_ports(ports_input):
    ports = set()
    for part in ports_input.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            if start.isdigit() and end.isdigit():
                ports.update(range(int(start), int(end)+1))
        elif part.isdigit():
            ports.add(int(part))
    return sorted([p for p in ports if 1 <= p <= 65535])

def scan_ports(target_ip, ports=None, timeout=1):
    if ports is None:
        ports = range(1, 1001)
    open_ports = []
    print(f"[INFO] Starting port scan on {target_ip} ({len(ports)} ports)")
    for port in ports:
        print(f"[SCAN] Testing port {port}", end='\r')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            result = s.connect_ex((target_ip, port))
            if result == 0:
                print(f"[OPEN] Open port: {port}")
                open_ports.append(port)
        except Exception as e:
            print(f"[ERROR] Port {port}: {e}")
        finally:
            s.close()
    print("\n[INFO] Scan finished.")
    if open_ports:
        print("[RESULT] Open ports:")
        for port in open_ports:
            print(port)
    else:
        print("[RESULT] No open ports found.")
    return open_ports
