import re
import os
import sys
import platform

def is_windows():
    return platform.system().lower() == "windows"

def is_valid_ip(ip):
    return re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip) is not None and all(0 <= int(x) <= 255 for x in ip.split("."))

def is_valid_port(port):
    return port.isdigit() and 1 <= int(port) <= 65535

def require_root():
    if not is_windows() and hasattr(os, "geteuid") and os.geteuid() != 0:
        print("[ERROR] This action requires root privileges. Please run with sudo.")
        sys.exit(1)

def confirm_action(message):
    resp = input(f"{message} (y/N): ").strip().lower()
    return resp == "y"

def get_int(prompt, default):
    try:
        value = input(prompt)
        if not value.strip():
            return default
        return int(value)
    except ValueError:
        print("[ERROR] Invalid number, using default.")
        return default
