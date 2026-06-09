# find if bgp port 179 is open?
# open from peer
# keepalive exchange (multithread?) to mainatin sess

from scapy.contrib.bgp import BGPHeader, BGPOpen
from conn.conn_socket import SocketConn
from misc.grab_settings import get_config
from misc.print_table import print_settings_table
from conn.parse_BGP import open_BGP


def conn_OPEN():

    config_dict = get_config(["version", "asn", "hold_time", "bgp_id", "neighbor_ip", "neighbor_port"])

    print_settings_table(config_dict)

    while True:
        send = (input("\n[*] Send BGP OPEN Packet (y/n): ")).lower()

        match send:
            case 'y':
                break
            case 'n':
                print("[x] Cancelling operation...\n")
                return 0
            case _:
                print("[x] Invalid option")

    open_msg = BGPOpen(
        version=int(config_dict["version"]),
        my_as=int(config_dict["asn"]),
        hold_time=int(config_dict["hold_time"]),
        bgp_id=str(config_dict["bgp_id"])
    )

    pkt = BGPHeader(type=1) / open_msg
    print("[+] BGP OPEN packet built")

    try:
        print("[*] Attempting 3 way handshake...")
        connection = SocketConn(config_dict["neighbor_ip"], int(config_dict["neighbor_port"]))
        print("[+] TCP connection Established")
    except:
        print("[-] Something went wrong")
        return None

    try:
        print("[*] Attempting to send OPEN BGP...")
        connection.send(pkt)
        print("[+] OPEN BGP sent")

        print("[*] Waiting for target response...")
        response = connection.recv()
        open_BGP(response)
        print("[+] Response received!")
    except:
        print("[-] Something went wrong!!")
        return None
    
    return connection