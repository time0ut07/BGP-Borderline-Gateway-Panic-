import json
import ipaddress
import os

RIB_FILE = "./resources/route.json"


def dig_RIB(target:str) -> dict:

    if not os.path.exists(RIB_FILE):
        return None

    with open(RIB_FILE, "r") as f:
        rib = json.load(f)

    #
    # Exact prefix lookup
    #
    if "/" in target:
        return rib.get(target)

    #
    # Host lookup
    #
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