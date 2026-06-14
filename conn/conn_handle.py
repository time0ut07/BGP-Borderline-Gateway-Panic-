from misc.logging import handle_log
from misc.grab_settings import get_config
from conn.parse_BGP import parse_update_BGP


def handle_keepalive(bgp):
    """
    Just logs keep alive
    """

    ip = get_config(["neighbor_ip"])["neighbor_ip"]
    handle_log(f"KEEPALIVE received from {ip}")

    return 0


def handle_notification(bgp):
    pass


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