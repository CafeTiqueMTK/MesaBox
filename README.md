# MesaBox

**MesaBox** is a Python-based pentest toolkit for Linux and Windows, featuring an interactive menu and a wide range of network utilities.

## Features

- **UDP Flood**: Generate configurable UDP traffic (target, duration, threads, rate, payload size).
- **TCP Flood**: Generate configurable TCP traffic (target, duration, threads, rate, payload size).
- **Ping**: Test connectivity to an IP address.
- **Local Network Scan**: Detect active IPs on the local network.
- **Wi-Fi BSSID/SSID Scan**: List nearby Wi-Fi access points (with optional JSON export).
- **Wi-Fi Deauth Attack**: Disconnect clients from an access point (requires monitor mode and root).
- **Port Scan**: Detect open ports on a target IP.
- **Network Interface Info**: Display network interfaces and details.
- **Clear BSSID/SSID List**: Reset the Wi-Fi database.
- **Interactive Menu**: Simple and clear navigation.

## Installation

### Linux (Debian/Ubuntu, Fedora, Arch, openSUSE)

```bash
git clone https://github.com/your-user/mesabox.git
cd mesabox
chmod +x install_all.sh
./install_all.sh
```

### Windows

Run `install_windows.bat` in an administrator terminal.

## Usage

```bash
sudo python3 main.py
```

**Note:** Some features (Wi-Fi, deauth, BSSID scan) require root privileges and/or a Wi-Fi interface in monitor mode.

## Structure

```
main.py
src/
  udp_flood.py
  tcp_flood.py
  ping_tool.py
  network_scanner.py
  bssid_scanner.py
  deauth_attack.py
  network_info.py
  wifi_network_scanner.py
  port_scanner.py
  __init__.py
README.md
install_all.sh
install_windows.bat
bssid_list.json
```

## Dependencies

- Python 3.x
- scapy
- wireless-tools or iw (Linux)
- iproute2 (Linux)
- pip (Linux/Windows)

## Warning

**Use these tools only on networks and devices you own or have explicit permission to test. Unauthorized use is illegal.**

---

© 2024 MesaBox  
Credit: Team DSU
