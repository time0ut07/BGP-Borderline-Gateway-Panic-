from misc.logging import handle_log
from misc.grab_config import get_config
from conn.parse_BGP import parse_update_BGP, connectivity
from scapy.contrib.bgp import *


ip = get_config(["neighbor_ip"])["neighbor_ip"]

TYPE_MAP = {
    1: "ORIGIN",
    2: "AS_PATH",
    3: "NEXT_HOP",
    4: "MULTI_EXIT_DISC",
    5: "LOCAL_PREF",
    8: "COMMUNITY",
}


def handle_keepalive(bgp):
    """
    Just logs keep alive
    """

    handle_log(f"KEEPALIVE received from {ip}")

    return 0


def handle_notification(bgp):
    
    msg = bgp[BGPNotification]

    # look at all error code and print somwthing for each
    print(msg.error_code, msg.error_subcode)
    print("HANDLE NOTIF")
    #connectivity()
    handle_log(f"NOTIFICATION received from {ip}")


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

def handle_update(bgp):
    print("\n[+] UPDATE received")
    print(bgp)
    update_msg = bgp.payload
    print(f"Withdrawn Routes Len: {update_msg.withdrawn_routes_len}\n")
    print(f"Withdrawn Routes: {update_msg.withdrawn_routes}\n")
    print(f"Path Attribute Len: {update_msg.path_attr_len}\n")
    print(f"Path Attribute: {update_msg.path_attr[0].type_flags}\n")

    # SEPERATE OBJ LIAO, NOW JUST WRITE IN ROUTE.TXT FOR RIB
    for field in update_msg.path_attr:
        match field.type_code:
            case 1: # origin
                print(field.attribute.origin) # 0 IGB, 1 EBG, 2 = others
            case 2: # as_path
                for segments in field.attribute.segments:
                    print(segments.segment_value)
            case 3: # next_hop
                print(field.attribute.next_hop)
            case _:
                print(TYPE_MAP.get(field.type_code, str(field.type_code)))

    print(f"NLRI:")
    for nlri in update_msg.nlri:
        print(nlri.prefix)
    
    parse_update_BGP(bgp)

def format_update(update):
    lines = []

    # NLRI (prefixes)
    prefixes = []
    for p in update.nlri:
        prefixes.append(str(p.prefix))

    # Path attributes
    as_path = "NA"
    next_hop = "NA"
    origin = "NA"
    med = "NA"

    for attr in update.path_attr:

        # ORIGIN
        if attr.type_code == "ORIGIN":
            origin = str(attr.attribute.origin)

        # AS_PATH
        elif attr.type_code == "AS_PATH":
            path = []
            for seg in attr.attribute.segments:
                path.extend(seg.segment_value)
            as_path = " ".join(map(str, path))

        # NEXT_HOP
        elif attr.type_code == "NEXT_HOP":
            next_hop = str(attr.attribute.next_hop)

        # MED
        elif attr.type_code == "MULTI_EXIT_DISC":
            med = str(attr.attribute.med)

    # Build final string output
    for pfx in prefixes:
        lines.append(
            f"{pfx} | NH:{next_hop} | AS_PATH:{as_path} | ORIGIN:{origin} | MED:{med}"
        )

    return lines