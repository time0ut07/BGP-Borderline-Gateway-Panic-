import json
import os
import ipaddress

RIB_FILE = "./resources/route.json"
"""str: File path to the local Routing Information Base (RIB) database"""


def add_route(params:dict) -> None:
    """Validate and add a static route to the local Routing Information Base

    Validates the required route parameters, parses optional BGP path
    attributes, loads the existing RIB from disk, inserts or updates the
    specified network prefix, and writes the modified routing table back to
    persistent storage.

    Args:
        params (dict): Dictionary containing route configuration values. The
            required keys are ``prefix`` and ``next_hop``. Optional keys
            include ``as_path``, ``origin``, and ``med``.
    """

    prefix = params.get("prefix")
    next_hop = params.get("next_hop")

    # prefix and next_hop are required
    if not prefix:
        print("[-] Missing required field: prefix")
        return

    if not next_hop:
        print("[-] Missing required field: next_hop")
        return

    # validate prefix
    try:
        ipaddress.ip_network(prefix, strict=False)
    except ValueError:
        print(f"[-] Invalid prefix: {prefix}")
        return

    # validate next_hop
    try:
        ipaddress.IPv4Address(next_hop)
    except ValueError:
        print(f"[-] Invalid next_hop: {next_hop}")
        return

    # parse optional fields
    as_path_raw = params.get("as_path", "")
    try:
        as_path = [int(asn) for asn in as_path_raw.split(",") if asn.strip()]
    except ValueError:
        print(f"[-] Invalid as_path: {as_path_raw}")
        return

    try:
        origin = int(params.get("origin", 0))  # default 0 = IGP
    except ValueError:
        print(f"[-] Invalid origin, must be 0, 1 or 2")
        return

    try:
        med = int(params.get("med", 0))  # default 0
    except ValueError:
        print(f"[-] Invalid med: {params.get('med')}")
        return

    # load existing RIB
    if os.path.exists(RIB_FILE) and os.path.getsize(RIB_FILE) > 0:
        with open(RIB_FILE, "r") as f:
            rib = json.load(f)
    else:
        rib = {}

    # append route
    rib[prefix] = {
        "as_path": as_path,
        "origin": origin,
        "next_hop": next_hop,
        "med": med
    }

    with open(RIB_FILE, "w") as f:
        json.dump(rib, f, indent=4)

    print(f"[+] Route added: {prefix} via {next_hop}")
    