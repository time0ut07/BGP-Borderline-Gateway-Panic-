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
| `config add-route` | Manually injects a route into the RIB | `config add-route prefix=10.0.0.0/24 next_hop=192.168.1.1` |

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
| `exit` | Gracefully shuts down the application | `exit` |