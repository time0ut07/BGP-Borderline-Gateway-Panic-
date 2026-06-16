from datetime import datetime
from scapy.contrib.bgp import BGP
from conn.conn_routing import update_route


PROFILE_FILE = "./resources/profile.log"


def connectivity():
    
    with open(PROFILE_FILE, "r") as f:
        lines = f.readlines()

    key = "Connectivity:"
    found = False
    new_lines = []

    for line in lines:
        if line.startswith(key):
            found = True
            value = line.split(":")[1].strip().lower()
            toggled = "False" if value == "true" else "True"
            new_lines.append(f"{key} {toggled}\n")
        else:
            new_lines.append(line)

    if not found:
        new_lines.append(f"{key} True\n")

    with open(PROFILE_FILE, "w") as f:
        f.writelines(new_lines)


def get_connectivity():

    with open(PROFILE_FILE, "r") as f:
        for line in f:
            if line.startswith("Connectivity:"):
                value = line.split(":")[1].strip().lower()
                if value == 'true':
                    return True

    return False


def parse_open_BGP(data: bytes) -> int:

    pkt = BGP(data)

    if pkt.type == 1:
        open_msg = pkt.payload

        with open(PROFILE_FILE, "a") as f:
            f.write(f"Timestamp: {datetime.now()}\n")
            f.write(f"Version: {open_msg.version}\n")
            f.write(f"ASN: {open_msg.my_as}\n")
            f.write(f"Hold Time: {open_msg.hold_time}\n")
            f.write(f"Router ID: {open_msg.bgp_id}\n")

    return 0


def parse_update_BGP(bgp) -> int:

    if bgp.type == 2:

        update_msg = bgp.payload
        # modify the route.txt with these info
        with open(PROFILE_FILE, "a") as f:
            f.write(f"Withdrawn Routes Len: {update_msg.withdrawn_routes_len}\n")
            f.write(f"Withdrawn Routes: {update_msg.withdrawn_routes}\n")
            f.write(f"Path Attribute Len: {update_msg.path_attr_len}\n")
            f.write(f"Path Attribute: {update_msg.path_attr}\n")
            f.write(f"NLRI: {update_msg.nlri}\n")

        update_route(update_msg)

    return 0