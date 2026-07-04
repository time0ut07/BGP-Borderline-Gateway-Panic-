ROUTE_FILE = "./resources/route.txt"
"""str: File path to the local text-based routing table database"""


def update_route(update_msg:object) -> None:
    """Update the local routing table using information from a BGP UPDATE message

    Loads the existing route database, removes any withdrawn prefixes, extracts
    supported path attributes such as NEXT_HOP and AS_PATH, updates advertised
    NLRI entries, and writes the resulting routing table back to persistent
    storage

    Args:
        update_msg: A parsed BGP UPDATE message containing withdrawn routes,
            path attributes, and newly advertised network prefixes
    """

    route_table = {}

    try:
        with open(ROUTE_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|")
                prefix = parts[0]
                route_table[prefix] = line

    except FileNotFoundError:
        pass

    # extraction
    next_hop = None
    as_path = None

    for attr in update_msg.path_attr:
        attr_type = getattr(attr, "type", None)

        # NEXT_HOP
        if attr_type == 3:
            next_hop = attr.value

        # AS_PATH
        elif attr_type == 2:
            as_path = attr.value

    # withdrawn routes
    for withdrawn in getattr(update_msg, "withdrawn_routes", []):
        prefix = str(withdrawn)
        if prefix in route_table:
            del route_table[prefix]

    # NLRI
    for nlri in getattr(update_msg, "nlri", []):
        prefix = str(nlri)

        entry = f"{prefix}|NH:{next_hop}|AS_PATH:{as_path}"
        route_table[prefix] = entry

    # write
    with open(ROUTE_FILE, "w") as f:
        for entry in route_table.values():
            f.write(entry + "\n")
