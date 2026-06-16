ROUTE_FILE = "./resources/route.txt"


def update_route(update_msg) -> None:
    """
    Maintains simple BGP-like routing table based on BGP UPDATE
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