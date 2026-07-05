import threading
import re
import binascii
from scapy.contrib.bgp import BGPHeader
from typing import Optional

from conn.conn_socket import SocketConn
from conn.conn_handle import (
    handle_open, handle_keepalive, handle_notification, handle_update, handle_route_refresh
)


def get_open_bgp(conn: SocketConn) -> Optional[bytes]:
    """Retrieve and process the initial incoming BGP OPEN session establishment frame

    Blocks until a network frame payload arrives on the socket interface. If raw data 
    is received, it casts it as a standard BGPHeader layer to evaluate baseline session 
    connectivity variables

    Args:
        conn (SocketConn): The underlying active TCP control socket connecting the peer

    Returns:
        Optional[bytes]: The raw unparsed network byte string if received successfully, 
            or None if the socket returns empty context
    """

    response = conn.recv()

    if not response:
        return None

    bgp = BGPHeader(response)
    handle_open(bgp)
    
    return response


def run_receiver(conn:SocketConn) -> None:
    """Initialize and dispatch receive thread to receive all BGP packets

    Spawns a thread that receives BGP packets from neighbors

    Args:
        conn (SocketConn): The underlying active TCP control socket connecting the peer
    """

    try:
        print('[*] Attempting to run receiver in the background...')
        thread = threading.Thread(
            target=receive_BGP,
            args=(conn,),
            daemon=True
        )

        thread.start()
        print('[+] Receiver running in the background')

    except Exception as e:
        print("[x] Something went wrong [run_receiver]: ", e)


def receive_BGP(conn:SocketConn) -> None:
    """Continuously intercept network frames and reassemble coalesced BGP stream packages

    Reads raw streams off the underlying network socket interface, performs hexadecimal 
    regex splitting using the standard 16-byte BGP synchronization marker boundary 
    (0xFFFF...FFFF) to counter TCP aggregation anomalies, fragments individual payload arrays, 
    and routes them to dedicated type-code action controllers

    Args:
        conn (SocketConn): The underlying active TCP control socket connecting the peer
    """

    while True:

        try:
            response = conn.recv()

            if response is None:
                continue

            if not response:
                break

            bgp = BGPHeader(response)
            received_bytes = bytes(bgp).hex()
            seperate_bgp = ['ffffffffffffffffffffffffffffffff' + part for part in re.split(f'ffffffffffffffffffffffffffffffff', received_bytes) if part]

            for indiv_bgp_bytes in seperate_bgp:
                indiv_bgp = BGPHeader(bytes.fromhex(indiv_bgp_bytes))
                bgp_type_code = indiv_bgp.type

                match bgp_type_code:
                    case 1:
                        handle_open(indiv_bgp)
                    case 2:
                        handle_update(indiv_bgp)
                    case 3:
                        handle_notification(indiv_bgp)
                    case 4:
                        handle_keepalive(indiv_bgp)
                    case 5:
                        handle_route_refresh(indiv_bgp, conn)
                    case _:
                        print(f"[x] Received unknown bgp packet type")

        except ConnectionAbortedError as e:
            print(f"[x] Connection aborted [conn_receive]: {e}")
            break

        except ConnectionResetError as e:
            print(f"[x] Connection reset [conn_receive]: {e}")
            break

        except Exception as e:
            print(f"[x] Unexpected receive error [conn_receive]: {e}")
            break
            