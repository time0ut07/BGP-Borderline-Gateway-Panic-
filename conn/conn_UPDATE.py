from scapy.contrib.bgp import BGPHeader, BGPUpdate, BGPPathAttr, BGPPAASPath, BGPPANextHop, BGPPAOrigin, BGPNLRI_IPv4
from scapy.all import *
import threading

from conn.conn_socket import SocketConn
from misc.grab_config import get_config
from misc.print_table import print_config_table
from misc.logging import handle_log
from misc.bgp_utils import build_as_path_attr


def receive_UPDATE(conn:SocketConn) -> None:
    """Continuously receive incoming BGP UPDATE packets from a peer

    Listens for incoming data on the active TCP connection until the remote
    peer closes the connection or no further data is received

    Args:
        conn (SocketConn): The active BGP socket connection used to receive
            UPDATE messages
    """
    while True:
        data = conn.recv(4096)

        if not data:
            break


def thread_UPDATE() -> None:
    """Start background threads responsible for UPDATE reception and KEEPALIVE

    Creates daemon threads that continuously receive incoming UPDATE packets
    and periodically transmit KEEPALIVE messages using the negotiated hold
    timer derived from both BGP peers.
    """

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
        print("[x] Something went wrong [thread_UPDATE]: ", e)


def send_UPDATE(conn:SocketConn) -> None:
    """Construct and transmit a BGP UPDATE message to the connected peer

    Retrieves routing configuration, prompts for user confirmation, builds
    the required BGP path attributes and NLRI information, constructs a BGP
    UPDATE packet, and sends it over the active connection.

    Args:
        conn (SocketConn): The active BGP socket connection used to transmit
            UPDATE messages.

    Returns:
        None: The UPDATE packet is transmitted if construction and sending
            complete successfully.
    """

    # get configurations
    config_dict = get_config(['asn', 'neighbor_ip', 'nlri', 'bgp_id', 'target_asn'])
    print_config_table(config_dict)

    while True:
        # confirmation
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

    peer_supports_four_byte_asn = getattr(conn, "peer_supports_four_byte_asn", False)
    # update parameters
    try:
        as_path = build_as_path_attr(
            int(config_dict["asn"]),
            int(config_dict["target_asn"]),
            peer_supports_four_byte_asn
        )
    except ValueError as e:
        print(f"[-] Cannot build UPDATE: {e}")

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
        conn.send(pkt)
        handle_log(f"UPDATE send to {config_dict['bgp_id']}", "bgp.log")
        print("[+] UPDATE BGP sent")
    except Exception as e:
        print("[-] Something went wrong [send_UPDATE]:", e)
        return None

    return None


def send_empty_UPDATE(conn:SocketConn) -> None:
    """Send an empty BGP UPDATE message to the connected peer

    Constructs a BGP UPDATE packet containing no withdrawn routes, path
    attributes, or NLRI information. This is used to respond to ROUTE REFRESH
    requests

    Args:
        conn (SocketConn): The active BGP socket connection used to send the
            UPDATE message.
    """

    pkt = BGPHeader(type=2) / BGPUpdate(
        withdrawn_routes=[],
        path_attr=[],
        nlri=[]
    )

    conn.send(pkt)