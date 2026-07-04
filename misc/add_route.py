import json
import os
import ipaddress

RIB_FILE = "./resources/route.json"
"""str: File path to the local Routing Information Base (RIB) database"""


def add_route(params: dict) -> None:
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

    # prefix must include a mask
    if "/" not in prefix:
        print(f"[-] Invalid prefix: {prefix} — must include prefix length (e.g. 10.0.0.0/24)")
        return

    # validate and normalise prefix
    try:
        network = ipaddress.ip_network(prefix, strict=False)
        prefix = str(network)  # normalise to network address
    except ValueError:
        print(f"[-] Invalid prefix: {prefix}")
        return

    # validate prefix length
    if not (0 <= network.prefixlen <= 32):
        print(f"[-] Invalid prefix length: /{network.prefixlen} — must be between 0 and 32")
        return

    # validate next_hop
    try:
        nh = ipaddress.IPv4Address(next_hop)
    except ValueError:
        print(f"[-] Invalid next_hop: {next_hop}")
        return

    if nh.is_loopback:
        print(f"[-] Invalid next_hop: {next_hop} — cannot be a loopback address")
        return

    if str(nh) == "0.0.0.0":
        print(f"[-] Invalid next_hop: {next_hop} — cannot be 0.0.0.0")
        return

    if nh == ipaddress.IPv4Address("255.255.255.255"):
        print(f"[-] Invalid next_hop: {next_hop} — cannot be broadcast address")
        return

    # parse and validate as_path
    as_path_raw = params.get("as_path", "")
    try:
        as_path = [int(asn) for asn in as_path_raw.split(",") if asn.strip()]
    except ValueError:
        print(f"[-] Invalid as_path: {as_path_raw} — must be comma separated integers")
        return

    for asn in as_path:
        if not (1 <= asn <= 4294967295):
            print(f"[-] Invalid ASN in as_path: {asn} — must be between 1 and 4294967295")
            return

    # parse and validate origin
    try:
        origin = int(params.get("origin", 0))
    except ValueError:
        print(f"[-] Invalid origin — must be 0 (IGP), 1 (EGP), or 2 (INCOMPLETE)")
        return

    if origin not in [0, 1, 2]:
        print(f"[-] Invalid origin: {origin} — must be 0 (IGP), 1 (EGP), or 2 (INCOMPLETE)")
        return

    # parse and validate med
    try:
        med = int(params.get("med", 0))
    except ValueError:
        print(f"[-] Invalid med: {params.get('med')} — must be an integer")
        return

    if not (0 <= med <= 4294967295):
        print(f"[-] Invalid med: {med} — must be between 0 and 4294967295")
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

def view_routes() -> None:
    """Display all routes currently stored in the local RIB.

    Reads the route.json file and prints each prefix with its associated
    path attributes in a formatted table.
    """

    if not os.path.exists(RIB_FILE) or os.path.getsize(RIB_FILE) == 0:
        print("[*] RIB is empty")
        return

    try:
        with open(RIB_FILE, "r") as f:
            rib = json.load(f)
    except (json.JSONDecodeError, ValueError):
        print("[x] route.json is empty or corrupted")
        return

    if not rib:
        print("[*] RIB is empty")
        return

    print(f"\n{'Prefix':<22} {'Next Hop':<18} {'AS Path':<20} {'Origin':<10} {'MED'}")
    print("-" * 80)

    origin_map = {0: "IGP", 1: "EGP", 2: "INCOMPLETE"}

    for prefix, info in rib.items():
        as_path = " ".join(str(a) for a in info.get("as_path", [])) or "-"
        next_hop = info.get("next_hop", "-")
        origin = origin_map.get(info.get("origin", 0), "-")
        med = info.get("med", "-")

        print(f"{prefix:<22} {next_hop:<18} {as_path:<20} {origin:<10} {med}")

    print()


def remove_route(params: dict) -> None:
    """Remove a route from the local RIB by prefix.

    Looks up the given prefix in route.json and removes it if found.
    Saves the updated RIB back to disk.

    Args:
        params (dict): Dictionary containing the prefix to remove.
            Required key is ``prefix``.
    """

    prefix = params.get("prefix")

    if not prefix:
        print("[-] Missing required field: prefix")
        return

    # normalise prefix
    try:
        network = ipaddress.ip_network(prefix, strict=False)
        prefix = str(network)
    except ValueError:
        print(f"[-] Invalid prefix: {prefix}")
        return

    if not os.path.exists(RIB_FILE) or os.path.getsize(RIB_FILE) == 0:
        print("[*] RIB is empty")
        return

    try:
        with open(RIB_FILE, "r") as f:
            rib = json.load(f)
    except (json.JSONDecodeError, ValueError):
        print("[x] route.json is empty or corrupted")
        return

    if prefix not in rib:
        print(f"[-] Route not found: {prefix}")
        return

    del rib[prefix]

    with open(RIB_FILE, "w") as f:
        json.dump(rib, f, indent=4)

    print(f"[+] Route removed: {prefix}")
    