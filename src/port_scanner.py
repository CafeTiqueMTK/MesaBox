import socket

def scan_ports(target_ip, ports=None, timeout=1):
    """
    Scan the given ports (or first 1000 if ports=None) on the target IP.
    Shows open ports.
    """
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

if __name__ == "__main__":
    ip = input("IP to scan: ")
    ports_input = input("Ports to scan (e.g. 22,80,443 or blank for 1-1000): ")
    if ports_input.strip():
        ports = [int(p.strip()) for p in ports_input.split(",") if p.strip().isdigit()]
    else:
        ports = None
    scan_ports(ip, ports)
