from misc.logging import handle_log
from misc.grab_config import get_config
from conn.parse_BGP import parse_update_BGP, connectivity
from scapy.contrib.bgp import *


ip = get_config(["neighbor_ip"])["neighbor_ip"]


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
    connectivity()
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
    parse_update_BGP(bgp)