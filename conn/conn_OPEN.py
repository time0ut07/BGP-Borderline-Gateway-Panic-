from scapy.contrib.bgp import (BGPHeader, BGPOpen, BGPOptParam, 
                                BGPCapability, BGPCapMultiprotocol, 
                                BGPCapFourBytesASN)

from misc.grab_config import get_config
from misc.print_table import print_config_table
from misc.logging import handle_log
from misc.bgp_utils import open_message_asn, peer_supports_four_byte_asn
from conn.conn_receive import get_open_bgp
from conn.conn_socket import SocketConn
from conn.parse_BGP import parse_open_BGP


def conn_OPEN() -> SocketConn | None:
    """Orchestrate the BGP connection initialization and configuration negotiation

    Fetches routing configuration parameters, presents a CLI verification table, 
    prompts for user confirmation, constructs a raw BGP type-1 (OPEN) header with standard 
    capabilities, completes a 3-way TCP handshake, and negotiates connection flags with 
    the remote peer

    Returns:
        SocketConn | None: An active network socket wrapper object if negotiation 
            is completely successful, or None if the operation is cancelled or errors.
    """

    # get configurations
    config_dict = get_config(["version", "asn", "hold_time", "bgp_id", "neighbor_ip", "neighbor_port"])

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

    # BGP OPEN PKT
    open_msg = BGPOpen(
        version=int(config_dict["version"]),
        my_as=open_message_asn(int(config_dict["asn"])),
        hold_time=int(config_dict["hold_time"]),
        bgp_id=str(config_dict["bgp_id"]),
        opt_params=[
            # Multiprotocol Extension
            BGPOptParam(
                param_type=2,
                param_value=BGPCapMultiprotocol(afi=1, safi=1)
            ),

            # Route Refresh Cisco (code 128)
            BGPOptParam(
                param_type=2,
                param_value=BGPCapability(code=128)
            ),

            # Route Refresh standard (code 2)
            BGPOptParam(
                param_type=2,
                param_value=BGPCapability(code=2)
            ),

            # Enhanced Route Refresh (code 70)
            BGPOptParam(
                param_type=2,
                param_value=BGPCapability(code=70)
            ),

            # 4-octet ASN support
            BGPOptParam(
                param_type=2,
                param_value=BGPCapFourBytesASN(asn=int(config_dict["asn"]))
            )
        ]
    )

    pkt = BGPHeader(type=1) / open_msg
    print("[+] BGP OPEN packet built")

    # 3 way handshake
    try:
        print("[*] Attempting 3 way handshake...")
        connection = SocketConn(
            config_dict["neighbor_ip"], 
            int(config_dict["neighbor_port"])
        )
        print("[+] TCP connection Established")

    except Exception as e:
        print("[-] Something went wrong [conn_OPEN - 3 way handshake]:", e)
        return None

    # sending BGP open
    try:
        print("[*] Attempting to send OPEN BGP...")
        connection.send(pkt)
        handle_log(f"OPEN packet sent to {config_dict['neighbor_ip']}", "bgp.log")
        print("[+] OPEN BGP sent")

        print("[*] Waiting for target response...")
        open_response = get_open_bgp(connection)
        connection.peer_supports_four_byte_asn = peer_supports_four_byte_asn(open_response)
        parse_open_BGP(open_response)

        handle_log(f"OPEN packet received from {config_dict["neighbor_ip"]}", "bgp.log")
        print("[+] Open response received!")

    except Exception as e:
        print("[-] Something went wrong [conn_OPEN - BGP Open send]:", e)
        return None
    
    return connection
    