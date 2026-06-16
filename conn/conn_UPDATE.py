from scapy.contrib.bgp import BGPHeader, BGPUpdate, BGPPathAttr, BGPPAASPath, BGPPANextHop, BGPPAOrigin, BGPNLRI_IPv4
from scapy.all import *
import threading

from misc.grab_config import get_config
from misc.print_table import print_config_table
from misc.logging import handle_log


def receive_UPDATE(conn):
    while True:
        data = conn.recv(4096)
        print(data)

        if not data:
            break


def thread_UPDATE():

    thread = threading.Thread(
        target=receive_UPDATE,
        args=(conn,),
        daemon=True
    )

    thread.start()


    with open("./resources/profile.log", "r") as f:
        for line in f:
            line = line.strip().split(": ")
            
            if line[0] == "Hold Time":
                target_hold_time = int(line[1])
                break

    our_hold_time = int(get_config(["hold_time"])["hold_time"])
    negotiated_hold_time = min(our_hold_time, target_hold_time) / 3

    try:
        print("[+] Attempting to run KEEPALIVE in the background...")
        thread = threading.Thread(
            target=conn_KEEPALIVE,
            args=(conn, negotiated_hold_time),
            daemon=True
        )

        thread.start()

    except Exception as e:
        print("[x] Something went wrong: ", e)

    return 0


def send_UPDATE(conn):

    config_dict = get_config(['asn', 'neighbor_ip', 'nlri', 'bgp_id'])

    print_config_table(config_dict)

    while True:
        send = (input("\n[*] Send BGP OPEN Packet (y/n): ")).lower()

        match send:
            case 'y':
                break
            case 'n':
                print("[x] Cancelling operation...\n")
                return None
            case _:
                print("[x] Invalid option")
                continue

    as_path = BGPPathAttr(
        type_flags=0x40,
        type_code=2,
        attribute=BGPPAASPath(segments=[
            BGPPAASPath.ASPathSegment(segment_type=2, segment_value=[int(config_dict["asn"])])
        ])
    )

    next_hop = BGPPathAttr(
        type_flags=0x40,
        type_code=3,
        attribute=BGPPANextHop(next_hop=config_dict['bgp_id'])
    )

    origin = BGPPathAttr(
        type_flags=0x40,
        type_code=1,
        attribute=BGPPAOrigin(origin=0)
    )

    nlri = BGPNLRI_IPv4(prefix=config_dict["nlri"])  # must include /mask

    update_msg = BGPUpdate(
        withdrawn_routes=[],
        path_attr=[as_path, next_hop, origin],
        nlri=[nlri]
    )

    pkt = BGPHeader(type=2) / update_msg
    print("[+] BGP UPDATE packet built")

    try:
        print("[*] Attempting to send UPDATE BGP...")
        print(raw(pkt).hex())
        conn.send(pkt)
        handle_log(f"UPDATE send to {config_dict['bgp_id']}")
        print("[+] UPDATE BGP sent")
    except Exception as e:
        print("[-] Something went wrong UPDATE:", e)
        return None

    return None