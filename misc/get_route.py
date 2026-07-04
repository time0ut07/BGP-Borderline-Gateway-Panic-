import json
import ipaddress
import os

RIB_FILE = "./resources/route.json"
"""str: File path to the local Routing Information Base (RIB) database"""


def dig_RIB(target:str) -> dict | None:
    """Perform a routing table lookup in the local RIB

    Supports both exact prefix matching and longest-prefix match (LPM)
    lookups. If the input is a CIDR prefix, an exact match is attempted.
    Otherwise, the function treats the input as a host IP address and
    performs longest-prefix matching across all stored routes.

    Args:
        target (str): Either a CIDR prefix (e.g., "192.168.0.0/24") or a
            host IP address (e.g., "192.168.0.1").

    Returns:
        dict | None: The matching route entry. For LPM lookups, includes the
            selected prefix and its associated route metadata. Returns None
            if no match is found or the RIB file does not exist.
    """

    if not os.path.exists(RIB_FILE):
        return None

    with open(RIB_FILE, "r") as f:
        rib = json.load(f)

    # extract prefix lookup
    if "/" in target:
        return rib.get(target)

    # host lookup
    target_ip = ipaddress.ip_address(target)

    best_match = None
    best_prefix_len = -1

    for prefix, route_info in rib.items():

        network = ipaddress.ip_network(prefix, strict=False)

        if target_ip in network:

            if network.prefixlen > best_prefix_len:
                best_match = {
                    "prefix": prefix,
                    **route_info
                }
                best_prefix_len = network.prefixlen

    return best_match
