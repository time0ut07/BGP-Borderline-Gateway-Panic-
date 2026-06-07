from scapy.all import *


def three_way_handshake(target_ip:str, port:int=179):
    """
    3 Way Handshake
    """

    sport = RandShort()

    ip = IP(dst=target_ip)
    syn = TCP(sport=sport, dport=port, flags="S", seq=1000)

    synack = sr1(ip/syn, timeout=3)

    if not synack:
        print("[x] No SYN-ACk received...")
        return None

    ack = TCP(
        sport=sport,
        dport=port,
        flags="A",
        seq=synack.ack,
        ack=synack.seq + 1
    )

    send(ip/ack)

    print("[+] TCP Handshake Completed")

    return {
        "ip": ip,
        "sport": sport,
        "dport": port,
        "seq": synack.ack,
        "ack": synack.seq + 1
    }