from datetime import datetime
from scapy.contrib.bgp import BGP


def open_BGP(data: bytes) -> int:

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