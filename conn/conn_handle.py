import json
import os
from scapy.contrib.bgp import BGPHeader, BGPNotification

from misc.logging import handle_log
from misc.grab_config import get_config
from misc.status import change_status
from conn.parse_BGP import parse_update_BGP
from conn.conn_decoding import decode_bgp_notification
from conn.conn_UPDATE import send_empty_UPDATE

RIB_FILE = './resources/route.json'
"""str: File path to local Routing Information Base (RIB)"""

ip = get_config(["neighbor_ip"])["neighbor_ip"]
"""str: Cached IP address of the target BGP neighbor peer"""

TYPE_MAP = {
    1: "ORIGIN",
    2: "AS_PATH",
    3: "NEXT_HOP",
    4: "MULTI_EXIT_DISC",
    5: "LOCAL_PREF",
    8: "COMMUNITY",
}
"""dict[int, str]: Mapping of BGP path attribute type codes to names per RFC 4271"""


def handle_open(bgp:BGPHeader) -> None:
    """Handle incoming BGP OPEN session packets and register connectivity state

    Sets the internal configuration operational status and immediately inspects the 
    packet boundary for nested BGP notification layers

    Args:
        bgp (BGPHeader): The raw Scapy BGP header object container
    """

    change_status('bgp_connection', 1)

    if BGPNotification in bgp:
        handle_notification(bgp)


def handle_keepalive(bgp:BGPHeader) -> None:
    """Log passive BGP KEEPALIVE confirmation packets from the peer

    Args:
        bgp (BGPHeader): The raw Scapy BGP header object container
    """

    handle_log(f"KEEPALIVE received from {ip}", "bgp.log")


def handle_notification(bgp:BGPHeader) -> None:
    """Process an error notification packet and teardown active connections

    Extracts error codes, decodes them to human-readable strings, flags the local 
    connection state matrix as inactive

    Args:
        bgp (BGPHeader): The raw Scapy BGP header object container
    """

    msg = bgp[BGPNotification]
    change_status('bgp_connection', 0)

    error_msg = decode_bgp_notification(msg.error_code, msg.error_subcode)
    notification_msg = (
        f"NOTIFICATION received from {ip}: "
        f"{error_msg} (code={msg.error_code}, subcode={msg.error_subcode})"
    )

    print(f"[x] {notification_msg}")
    handle_log(notification_msg, "bgp.log")


def handle_update(bgp:BGPHeader) -> None:
    """Parse incoming BGP UPDATE packets and dynamically update the local RIB database

    Reads the current JSON RIB database file, removes explicitly withdrawn routes, 
    extracts standardized path attributes (such as AS_PATH, ORIGIN, NEXT_HOP, and MED), 
    and inserts or updates active NLRI fields before writing changes back to disk

    Args:
        bgp (BGPHeader): The raw Scapy BGP header object container
    """

    print("\n[+] Received UPDATE packet")

    print("\n[+] Received UPDATE packet")
    update_msg = bgp.payload

    # load existing RIB
    if os.path.exists(RIB_FILE) and os.path.getsize(RIB_FILE) > 0:
        with open(RIB_FILE, "r") as f:
            rib = json.load(f)
    else:
        rib = {}

    # handle WITHDRAWN routes
    if update_msg.withdrawn_routes_len > 0:

        for route in update_msg.withdrawn_routes:

            prefix = str(route.prefix)

            if prefix in rib:
                del rib[prefix]
                print(f"[-] Withdrawn: {prefix}")
            else:
                print(f"[!] Withdrawn route not found: {prefix}")

    # extract path attributes
    origin = None
    as_path = []
    next_hop = None
    med = None

    for field in update_msg.path_attr:

        match field.type_code:

            case 1:  # ORIGIN
                origin = field.attribute.origin

            case 2:  # AS_PATH
                for segment in field.attribute.segments:
                    as_path.extend(segment.segment_value)

            case 3:  # NEXT_HOP
                next_hop = field.attribute.next_hop

            case 4:  # MED
                med = field.attribute.med

    # add/update NLRI
    for nlri in update_msg.nlri:

        prefix = str(nlri.prefix)

        rib[prefix] = {
            "as_path": as_path,
            "origin": origin,
            "next_hop": next_hop,
            "med": med
        }

        print(f"[+] Route updated: {prefix}")

    # write file
    with open(RIB_FILE, "w") as f:
        json.dump(rib, f, indent=4)


def handle_route_refresh(bgp:BGPHeader, conn:any) -> None:
    """Process a BGP ROUTE REFRESH request message from a network peer

    Logs the incoming packet and responds by pushing an empty BGP UPDATE packet 

    Args:
        bgp (BGPHeader): The raw Scapy BGP header object container
        conn (socket.socket): The underlying active TCP control socket connecting the peer
    """
    
    handle_log(f"ROUTE REFRESH received from {ip}", "bgp.log")
    send_empty_UPDATE(conn)
