from scapy.all import sniff, IP, ICMP, TCP, UDP, ARP, Ether
import threading
from misc.timestamp import timestamp
from misc.grab_config import get_config
from misc.logging import handle_log
from misc.status import get_status, change_status
from scapy.all import AsyncSniffer

sniffer = None


def receive_sniffer(pkt):

    # BLOCK BGP (TCP port 179)
    if TCP in pkt:
        if pkt[TCP].sport == 179 or pkt[TCP].dport == 179:
            return

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
            prn=receive_sniffer,
            store=False,
            filter="ip or arp",
            promisc=True
        )
        sniffer.start()
        print("[+] Sniffing started")

        return sniffer

    # TOGGLE OFF
    else:
        if get_status('sniff') is False:
            print("[*] Sniffing is disabled already")
            return None

        change_status('sniff', 0)

        if sniffer is not None:
            sniffer.stop()
            sniffer = None
            print("[-] Sniffing stopped")

        return None