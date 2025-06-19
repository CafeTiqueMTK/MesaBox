#!/bin/bash

set -e

echo "Détection du gestionnaire de paquets..."

if command -v apt >/dev/null 2>&1; then
    echo "Gestionnaire détecté : apt (Debian/Ubuntu)"
    sudo apt update
    sudo apt install -y python3-pip wireless-tools iproute2 scapy 
elif command -v dnf >/dev/null 2>&1; then
    echo "Gestionnaire détecté : dnf (Fedora/RHEL)"
    sudo dnf install -y python3-pip iw iproute scapy
elif command -v pacman >/dev/null 2>&1; then
    echo "Gestionnaire détecté : pacman (Arch/Manjaro)"
    sudo pacman -Sy --noconfirm python-pip wireless_tools iproute2 scapy
elif command -v zypper >/dev/null 2>&1; then
    echo "Gestionnaire détecté : zypper (openSUSE)"
    sudo zypper install -y python3-pip wireless-tools iproute2 scapy
else
    echo "Aucun gestionnaire de paquets compatible détecté."
    exit 1
fi

echo "Installation des dépendances Python (scapy)..."
pip3 install --user scapy

echo "Installation terminée."
