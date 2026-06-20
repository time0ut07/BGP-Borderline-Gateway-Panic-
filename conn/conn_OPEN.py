from scapy.contrib.bgp import (BGPHeader, BGPOpen, BGPOptParam, 
                                BGPCapability, BGPCapMultiprotocol, 
                                BGPCapFourBytesASN)
from conn.conn_socket import SocketConn
from misc.grab_config import get_config
from misc.print_table import print_config_table
from conn.parse_BGP import parse_open_BGP
from misc.logging import handle_log
from conn.conn_receive import get_open_bgp


def conn_OPEN():

    config_dict = get_config(["version", "asn", "hold_time", "bgp_id", "neighbor_ip", "neighbor_port"])

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

    open_msg = BGPOpen(
        version=int(config_dict["version"]),
        my_as=int(config_dict["asn"]),
        hold_time=int(config_dict["hold_time"]),
        bgp_id=str(config_dict["bgp_id"]),
        opt_params=[
            # 1. Multiprotocol Extension
            BGPOptParam(
                param_type=2,
                param_value=BGPCapMultiprotocol(afi=1, safi=1)
            ),

            # 2. Route Refresh Cisco (code 128)
            BGPOptParam(
                param_type=2,
                param_value=BGPCapability(code=128)
            ),

            # 3. Route Refresh standard (code 2)
            BGPOptParam(
                param_type=2,
                param_value=BGPCapability(code=2)
            ),

            # 4. Enhanced Route Refresh (code 70)
            BGPOptParam(
                param_type=2,
                param_value=BGPCapability(code=70)
            ),

            # 5. 4-octet ASN support
            BGPOptParam(
                param_type=2,
                param_value=BGPCapFourBytesASN(asn=int(config_dict["asn"]))
            )
        ]
    )

    pkt = BGPHeader(type=1) / open_msg
    print("[+] BGP OPEN packet built")

    try:
        print("[*] Attempting 3 way handshake...")
        connection = SocketConn(
            config_dict["neighbor_ip"], 
            int(config_dict["neighbor_port"])
        )
        print("[+] TCP connection Established")

    except Exception as e:
        print("[-] Something went wrong:", e)
        return None

    try:
        print("[*] Attempting to send OPEN BGP...")
        connection.send(pkt)
        handle_log(f"OPEN packet sent to {config_dict['neighbor_ip']}", "bgp.log")
        print("[+] OPEN BGP sent")

        print("[*] Waiting for target response...")
        open_response = get_open_bgp(connection)
        parse_open_BGP(open_response)

        handle_log(f"OPEN packet received from {config_dict["neighbor_ip"]}", "bgp.log")
        print("[+] Open response received!")
        #connectivity()

    except Exception as e:
        print("[-] Something went wrong:", e)
        return None
    
    return connection