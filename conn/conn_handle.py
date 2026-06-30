from misc.logging import handle_log
from misc.grab_config import get_config
from conn.parse_BGP import parse_update_BGP
from scapy.contrib.bgp import *
from misc.status import change_status
from conn.conn_decoding import decode_bgp_notification
from conn.conn_UPDATE import send_empty_UPDATE
import json
import os

RIB_FILE = './resources/route.json'


ip = get_config(["neighbor_ip"])["neighbor_ip"]

TYPE_MAP = {
    1: "ORIGIN",
    2: "AS_PATH",
    3: "NEXT_HOP",
    4: "MULTI_EXIT_DISC",
    5: "LOCAL_PREF",
    8: "COMMUNITY",
}


def handle_open(bgp):

    change_status('bgp_connection', 1)

    if BGPNotification in bgp:
        handle_notification(bgp)


def handle_keepalive(bgp):
    """
    Just logs keep alive
    """

    handle_log(f"KEEPALIVE received from {ip}", "bgp.log")

    return 0


def handle_notification(bgp):

    msg = bgp[BGPNotification]
    change_status('bgp_connection', 0)

    error_msg = decode_bgp_notification(msg.error_code, msg.error_subcode)
    notification_msg = (
        f"NOTIFICATION received from {ip}: "
        f"{error_msg} (code={msg.error_code}, subcode={msg.error_subcode})"
    )
    print(f"[x] {notification_msg}")
    handle_log(notification_msg, "bgp.log")


# withdrawn routes (routes that are removed) - remove from routing table
# as_path (describes how to reach a prefix)
#   List of AS numbers the route passed through
#   Used for loop prevention + best path selection

# next_hop - ip addr to forward packets to
# local_pref - higher = more preferred (inside IBGP)
# MED (Multi Exit Discriminator) - Lower = between ASes
# Origin - How route was learnt (IBGP, EBGP, Incomplete)
# NLRI (Network Layer Reachability Info) - actual routes being advertised
#   e.g. 10.10.10.0/24

# def handle_update(bgp):
#     print("\n[+] UPDATE received")

#     update_msg = bgp.payload
#     print(f"Withdrawn Routes Len: {update_msg.withdrawn_routes_len}\n")
#     print(f"Withdrawn Routes: {update_msg.withdrawn_routes}\n")
#     print(f"Path Attribute Len: {update_msg.path_attr_len}\n")
#     print(f"Path Attribute: {update_msg.path_attr[0].type_flags}\n")

#     # SEPERATE OBJ LIAO, NOW JUST WRITE IN ROUTE.TXT FOR RIB
#     for field in update_msg.path_attr:
#         match field.type_code:
#             case 1: # origin
#                 print(field.attribute.origin) # 0 IGB, 1 EBG, 2 = others
#             case 2: # as_path
#                 for segments in field.attribute.segments:
#                     print(segments.segment_value)
#             case 3: # next_hop
#                 print(field.attribute.next_hop)
#             case _:
#                 print(TYPE_MAP.get(field.type_code), field.attribute.med, "MED")

#     print(f"NLRI:")
#     for nlri in update_msg.nlri:
#         print(nlri.prefix)
    
#     parse_update_BGP(bgp)


def handle_update(bgp):
    print("\n[+] Received UPDATE packet")
    update_msg = bgp.payload

    # Load existing RIB
    if os.path.exists(RIB_FILE) and os.path.getsize(RIB_FILE) > 0:
        with open(RIB_FILE, "r") as f:
            rib = json.load(f)
    else:
        rib = {}

    #
    # Handle Withdrawn Routes
    #
    if update_msg.withdrawn_routes_len > 0:

        for route in update_msg.withdrawn_routes:

            prefix = str(route.prefix)

            if prefix in rib:
                del rib[prefix]
                print(f"[-] Withdrawn: {prefix}")
            else:
                print(f"[!] Withdrawn route not found: {prefix}")

    #
    # Extract Path Attributes
    #
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

    #
    # Add/Update NLRI
    #
    for nlri in update_msg.nlri:

        prefix = str(nlri.prefix)

        rib[prefix] = {
            "as_path": as_path,
            "origin": origin,
            "next_hop": next_hop,
            "med": med
        }

        print(f"[+] Route updated: {prefix}")

    #
    # Save RIB
    #
    with open(RIB_FILE, "w") as f:
        json.dump(rib, f, indent=4)


def handle_route_refresh(bgp, conn):
    handle_log(f"ROUTE REFRESH received from {ip}", "bgp.log")
    send_empty_UPDATE(conn)
