# VORTEX

A modular BGP simulation and network control CLI designed for experimenting with BGP session establishment, UPDATE processing, routing table manipulation, and post-session traffic analysis features such as packet sniffing and routing control.

This project emulates simplified BGP behavior using Scapy and a file-based routing system, combined with a command-driven interface for interactive control.

> ⚠️ This tool is intended strictly for **educational, research, and controlled lab environments**.

---

## Features

### BGP Session Engine
- Establish BGP OPEN sessions
- Exchange KEEPALIVE messages
- Send and process BGP UPDATE packets
- Handle NOTIFICATION errors and session teardown
- ASN negotiation (2-byte + RFC 6793 4-byte support)

---

### Routing System (RIB)
- Local Routing Information Base stored in JSON (`route.json`)
- Longest Prefix Match (LPM) lookup engine
- Dynamic route updates via BGP UPDATE messages
- Manual route injection via CLI
- Route withdrawal handling

---

### Post-Exploit Network Tools
- Live packet sniffing engine (`pe/sniffer`)
- Traffic routing manipulation module (`pe/routing`)
- Background thread execution
- Runtime toggling via CLI

---

### Configuration System
- File-based configuration (`resources/config.txt`)
- Runtime configuration editing
- Input validation:
  - ASN range checking
  - IPv4 validation
  - MAC validation
  - Port and timer validation
- Optional field handling

---

### Logging
- BGP session logs → `resources/bgp.log`
- Traffic logs → `resources/traffic.log`
- Session profile logs → `resources/profile.log`
- Timestamped event logging system

---

## Getting Started

### Requirements
- Python 3.10+
- Scapy
- tabulate
- Root/admin privileges (for raw sockets / sniffing)

### Install dependencies
```bash
pip install -r requirements.txt
```

### Running the tool
```bash
sudo python VORTEX.py
```

## Command Reference

### Connection Commands

| Command | Description | Example |
|--------|-------------|---------|
| `connection open` | Opens a BGP session and starts KEEPALIVE + receiver threads | `connection open` |
| `connection update` | Sends a BGP UPDATE over the active session | `connection update` |

---

### Configuration Commands

| Command | Description | Example |
|--------|-------------|---------|
| `config view` | Displays current configuration values | `config view` |
| `config change key=value` | Updates a configuration parameter | `config change hold_time=30` |
| `config add-route` | Manually add a route into the RIB | `config add-route prefix=10.0.0.0/24 next_hop=192.168.1.1` |
| `config view-routes` | View all routes in RIB | `config view-routes` |
| `config remove-route` | Remove specified route in RIB | `config remove-route prefix=10.0.0.0/24` |

---

### Post-Exploitation Commands

| Command | Description | Example |
|--------|-------------|---------|
| `post-exploit sniff on` | Starts packet sniffing engine | `post-exploit sniff on` |
| `post-exploit sniff off` | Stops packet sniffing engine | `post-exploit sniff off` |
| `post-exploit route on` | Enables routing engine | `post-exploit route on` |
| `post-exploit route off` | Disables routing engine | `post-exploit route off` |

---

### Log Management

| Command | Description | Example |
|--------|-------------|---------|
| `clear bgp` | Clears BGP log file | `clear bgp` |
| `clear traffic` | Clears traffic log file | `clear traffic` |

---

### System Commands

| Command | Description | Example |
|--------|-------------|---------|
| `help` | Displays all available commands and descriptions | `help` |
| `exit` | Gracefully shuts down the application | `exit` |


### Configuration Reference
| Key | Description | Example |
|-----|-------------|---------|
| `version` | BGP version | `4` |
| `port` | Local BGP port | `179` |
| `protocol` | Transport protocol | `tcp` |
| `asn` | Your AS number | `65003` |
| `hold_time` | BGP hold time in seconds | `90` |
| `bgp_id` | Your BGP router IP | `192.168.1.1` |
| `neighbor_ip` | Peer router IP address | `192.168.1.2` |
| `neighbor_asn` | Peer router AS number | `65002` |
| `neighbor_port` | Peer BGP port | `179` |
| `nlri` | Prefix to advertise in BGP UPDATE | `10.0.0.0/24` |
| `iface` | Network interface for sniffing and routing | `eth0` |
| `route_dest_ip` | Routing destination IP (0.0.0.0 for blackhole) | `0.0.0.0` |
| `route_dest_mac` | Destination MAC address for forward mode | `aa:bb:cc:dd:ee:ff` |
