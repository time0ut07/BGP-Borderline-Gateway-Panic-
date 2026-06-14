from datetime import datetime
from scapy.contrib.bgp import BGP
from conn.conn_routing import update_route


def parse_open_BGP(data: bytes) -> int:

    pkt = BGP(data)

    if pkt.type == 1:
        open_msg = pkt.payload

        with open("./resources/profile.log", "a") as f:
            f.write(f"Timestamp: {datetime.now()}\n")
            f.write(f"Version: {open_msg.version}\n")
            f.write(f"ASN: {open_msg.my_as}\n")
            f.write(f"Hold Time: {open_msg.hold_time}\n")
            f.write(f"Router ID: {open_msg.bgp_id}\n")

    return 0


def parse_update_BGP(bgp) -> int:

    if bgp.type == 2:

        update_msg = bgp.payload

        with open("./resources/profile.log", "a") as f:
            f.write(f"Withdrawn Routes Len: {update_msg.withdrawn_routes_len}\n")
            f.write(f"Withdrawn Routes: {update_msg.withdrawn_routes}\n")
            f.write(f"Path Attribute Len: {update_msg.path_attr_len}\n")
            f.write(f"Path Attribute: {update_msg.path_attr}\n")
            f.write(f"NLRI: {update_msg.nlri}\n")

        update_route(update_msg)

    return 0