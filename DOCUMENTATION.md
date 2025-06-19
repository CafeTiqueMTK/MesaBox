# MesaBox Documentation

MesaBox is a modular network pentest toolkit written in Python.  
This documentation describes each tool, usage, and options.

---

## Table of Contents

- [General Usage](#general-usage)
- [Menu Options](#menu-options)
- [Modules](#modules)
  - [UDP Flood](#udp-flood)
  - [TCP Flood](#tcp-flood)
  - [Ping](#ping)
  - [Local Network Scan](#local-network-scan)
  - [Wi-Fi BSSID/SSID Scan](#wi-fi-bssidsid-scan)
  - [Wi-Fi Deauth Attack](#wi-fi-deauth-attack)
  - [External IP Scan](#external-ip-scan)
  - [Port Scanner](#port-scanner)
  - [Show Network Interfaces](#show-network-interfaces)
- [Requirements](#requirements)
- [Notes](#notes)
- [Credits](#credits)

---

## General Usage

Run the main menu with:

```bash
sudo python3 main.py
```

Some features require root privileges.

---

## Menu Options

1. **UDP Flood**  
   Flood a target IP/port with UDP packets.  
   Options: target IP, port, duration, packets/sec, threads, request weight.

2. **TCP Flood**  
   Flood a target IP/port with TCP connections.  
   Options: target IP, port, duration, packets/sec, threads, request weight.

3. **Ping an IP**  
   Send ICMP echo requests to test reachability.

4. **Scan local network**  
   Scan a local subnet for active hosts.

5. **Scan Wi-Fi BSSID/SSID**  
   List nearby Wi-Fi access points (optionally save to JSON).

6. **Wi-Fi Deauth Attack**  
   Send deauthentication frames to disconnect clients (requires monitor mode).

7. **Clear saved BSSID/SSID list**  
   Remove the saved Wi-Fi JSON file.

8. **Show network interfaces**  
   Display all network interfaces and their details.

9. **Scan external network IPs (by prefix)**  
   Ping all hosts in a given /24 subnet (e.g., 8.8.8.0/24).

10. **Scan ports of an IP**  
    Scan a range or list of ports on a target IP.

0. **Quit**  
   Exit MesaBox.

---

## Modules

### UDP Flood

- **File:** `src/udp_flood.py`
- **Description:** Sends UDP packets to a target at a configurable rate and size.
- **Usage:**  
  - Target IP/port  
  - Duration (seconds)  
  - Packets per second  
  - Threads  
  - Request weight (1 = small, 10 = large payload)

### TCP Flood

- **File:** `src/tcp_flood.py`
- **Description:** Opens TCP connections and sends data to a target at a configurable rate and size.
- **Usage:**  
  - Target IP/port  
  - Duration (seconds)  
  - Packets per second  
  - Threads  
  - Request weight (1 = small, 10 = large payload)

### Ping

- **File:** `src/ping_tool.py`
- **Description:** Sends ICMP echo requests to a target IP.

### Local Network Scan

- **File:** `src/network_scanner.py`
- **Description:** Scans a local subnet for active hosts using ping.

### Wi-Fi BSSID/SSID Scan

- **File:** `src/bssid_scanner.py`
- **Description:** Lists nearby Wi-Fi access points (BSSID/SSID) using `iwlist` or `iw`.  
  Optionally saves results to `bssid_list.json`.

### Wi-Fi Deauth Attack

- **File:** `src/deauth_attack.py`
- **Description:** Sends deauthentication frames to disconnect clients from an AP.  
  Requires monitor mode and root.

### External IP Scan

- **File:** `src/wifi_network_scanner.py`
- **Description:** Pings all IPs in a given /24 subnet (e.g., 8.8.8.0/24).

### Port Scanner

- **File:** `src/port_scanner.py`
- **Description:** Scans a list or range of ports on a target IP.

### Show Network Interfaces

- **File:** `src/network_info.py`
- **Description:** Displays all network interfaces and their configuration.

---

## Requirements

- Python 3.x
- scapy
- wireless-tools or iw (Linux)
- iproute2 (Linux)
- pip (Linux/Windows)
- Root privileges for some features

---

## Notes

- Use only on networks and devices you own or have explicit permission to test.
- Some features are Linux-only and require a compatible Wi-Fi card.
- For Wi-Fi attacks, your interface must be in monitor mode.

---

## Credits

MesaBox by Team DSU  
2025