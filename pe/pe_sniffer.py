from scapy.all import sniff, IP, ICMP, TCP, UDP, ARP, Ether, AsyncSniffer, sendp, get_if_hwaddr
import threading
from misc.timestamp import timestamp
from misc.grab_config import get_config
from misc.logging import handle_log
from misc.status import get_status, change_status
from scapy.all import AsyncSniffer
from pe.pe_routing import get_routing_handler

sniffer = None
routing_handler = None

def monitor_routing():
    global routing_handler
    routing_handler = get_routing_handler()
    import time
    while get_status('routing') is True:
        print("YES")
        time.sleep(2)

def run_routing(toggle):
    global routing_thread, routing_handler

    if get_status('bgp_connection') is not True:
        print("[x] Establish a BGP connection first")
        return None
    
    if toggle is True:
        if get_status('routing') is True:
            print("[*] Routing is enabled already")
            return None

        if get_status('sniff') is not True:
            print("[*] Sniffer not running, running it first")
            run_sniffer(True)
        
        change_status('routing', 1)

        # routing_thread = threading.Thread(
        #     target=monitor_routing,
        #     daemon=True
        # )

        # routing_thread.start()
        monitor_routing()
        print("[+] Routing started")

    else:
        if get_status('routing') is False:
            print("[*] Routing is disabled already")
            return None
        
        change_status('routing', 0)

        # if routing_thread is not None:
        #     routing_thread.join(timeout=2)
        #     routing_thread = None
        #     print("[-] Routing stopped")
        routing_handler = None
        print("[-] Routing stopped")


def log_sniffer(pkt):

    # BLOCK BGP (TCP port 179)
    if TCP in pkt:
        if pkt[TCP].sport == 179 or pkt[TCP].dport == 179:
            return

    if get_status('routing') is True and routing_handler is not None:
        routing_handler(pkt)
    log_msg = ""

    # Ethernet layer
    if Ether in pkt:
        log_msg += f"{pkt[Ether].src} -> {pkt[Ether].dst} | "

    # IP layer
    if IP in pkt:
        ip_src = pkt[IP].src
        ip_dst = pkt[IP].dst
        proto = pkt[IP].proto

        if ICMP in pkt:
            icmp = pkt[ICMP]
            log_msg += f"ICMP {ip_src} -> {ip_dst} | type={icmp.type} code={icmp.code}"

        elif TCP in pkt:
            tcp = pkt[TCP]
            log_msg += f"TCP {ip_src}:{tcp.sport} -> {ip_dst}:{tcp.dport} | flags={tcp.flags}"

        elif UDP in pkt:
            udp = pkt[UDP]
            log_msg += f"UDP {ip_src}:{udp.sport} -> {ip_dst}:{udp.dport} | len={len(pkt)}"

        else:
            log_msg += f"IP-{proto} {ip_src} -> {ip_dst} | len={len(pkt)}"

    elif ARP in pkt:
        arp = pkt[ARP]
        op = "Request" if arp.op == 1 else "Reply"
        log_msg += f"ARP {op} | {arp.psrc} -> {arp.pdst}"

    else:
        log_msg += f"OTHER | {pkt.summary()}"

    handle_log(log_msg, "traffic.log")


def run_sniffer(toggle):
    """
    Starts/stops Scapy sniffer using AsyncSniffer
    """
    global sniffer
    global routing_thread

    if get_status('bgp_connection') is not True:
        print("[x] Establish a BGP connection first")
        return None

    # TOGGLE ON
    if toggle is True:
        if get_status('sniff') is True:
            print("[*] Sniffing is enabled already")
            return sniffer

        change_status('sniff', 1)

        sniffer = AsyncSniffer(
            iface=get_config(['iface'])['iface'],
            prn=log_sniffer,
            store=False,
            #filter="ip or arp",
            promisc=True
        )
        sniffer.start()
        
        # routing_thread = threading.Thread(
        #     target=monitor_routing, 
        #     daemon=True
        # )

        # routing_thread.start()

        print("[+] Sniffing started")

        return sniffer

    # TOGGLE OFF
    else:
        if get_status('sniff') is False:
            print("[*] Sniffing is disabled already")
            return None

        change_status('sniff', 0)

        # if get_status('routing') is True:
        #     print("[*] Stopping routing as sniffer is being disabled...")
        #     monitor_routing(False)

        if sniffer is not None:
            sniffer.stop()
            sniffer = None
            print("[-] Sniffing stopped")

        return None