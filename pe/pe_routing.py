from scapy.all import send, sendp, IP, TCP, UDP, Ether, getmacbyip
from misc.grab_config import get_config
from misc.get_route import dig_RIB
from misc.logging import handle_log
from scapy.all import getmacbyip


def is_hijacked(dst_ip: str) -> bool:
    """
    checks if destination IP falls within any hijacked prefix in rib
    """
    result = dig_RIB(dst_ip)
    return result is not None


def get_routing_handler():
    config = get_config(["route_dest_ip", "iface"])
    pe_route_dest = config["route_dest_ip"]
    iface = config["iface"]
    is_blackhole = pe_route_dest == "0.0.0.0"

    # get MAC of destination upfront
    dest_mac = getmacbyip(pe_route_dest) if not is_blackhole else None
    if not is_blackhole and dest_mac is None:
        print(f"[x] Could not resolve MAC for {pe_route_dest}")
        return None

    def process_packet(pkt):
        if IP not in pkt:
            print("No IP Layer, Skipping")
            return

        dst = pkt[IP].dst
        src = pkt[IP].src
        print(f"process_packet called: {src} -> {dst}")

        if not is_hijacked(dst):
            return

        route = dig_RIB(dst)
        prefix = route.get("prefix", dst)

        if is_blackhole:
            print(f"[+] BLACKHOLE: {src} -> {dst} (prefix: {prefix}) — dropped")
            handle_log(f"BLACKHOLE: {src} -> {dst} (prefix: {prefix})", "pe.log")

        else:
            print(f"[+] FORWARD: {src} -> {dst} redirected to {pe_route_dest} (prefix: {prefix})")
            handle_log(f"FORWARD: {src} -> {dst} -> {pe_route_dest} (prefix: {prefix})", "pe.log")

            # rewrite destination
            pkt[IP].dst = pe_route_dest
            del pkt[IP].chksum

            if TCP in pkt:
                del pkt[TCP].chksum
            elif UDP in pkt:
                del pkt[UDP].chksum

            # rewrite ethernet layer with correct MAC
            pkt[Ether].dst = dest_mac
            del pkt[Ether].src

            sendp(pkt, iface=iface, verbose=False)

    return process_packet
