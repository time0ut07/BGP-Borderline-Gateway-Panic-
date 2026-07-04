from datetime import datetime
from scapy.contrib.bgp import BGP

from conn.conn_routing import update_route


PROFILE_FILE = "./resources/profile.log"
"""str: File path used to store parsed BGP session and routing profile information"""


def parse_open_BGP(data: bytes) -> None:
    """Parse an incoming BGP OPEN message and record peer information

    Decodes the raw BGP OPEN packet, extracts session negotiation parameters,
    and appends the peer's capabilities and identifying information to the
    local profile log.

    Args:
        data (bytes): Raw bytes containing a serialized BGP OPEN message.
    """

    pkt = BGP(data)

    if pkt.type == 1:
        open_msg = pkt.payload

        with open(PROFILE_FILE, "a") as f:
            f.write(f"Timestamp: {datetime.now()}\n")
            f.write(f"Version: {open_msg.version}\n")
            f.write(f"ASN: {open_msg.my_as}\n")
            f.write(f"Hold Time: {open_msg.hold_time}\n")
            f.write(f"Router ID: {open_msg.bgp_id}\n")


def parse_update_BGP(bgp:BGP) -> None:
    """Parse an incoming BGP UPDATE message and update local routing records

    Extracts routing information from the UPDATE message, appends the packet
    contents to the local profile log, and updates the local routing table
    with newly advertised and withdrawn network prefixes.

    Args:
        bgp (BGP): A parsed Scapy BGP packet containing an UPDATE message.
    """

    if bgp.type == 2:

        update_msg = bgp.payload
        # modify the route.txt with these info
        with open(PROFILE_FILE, "a") as f:
            f.write(f"Withdrawn Routes Len: {update_msg.withdrawn_routes_len}\n")
            f.write(f"Withdrawn Routes: {update_msg.withdrawn_routes}\n")
            f.write(f"Path Attribute Len: {update_msg.path_attr_len}\n")
            f.write(f"Path Attribute: {update_msg.path_attr}\n")
            f.write(f"NLRI: {update_msg.nlri}\n")

        update_route(update_msg)
