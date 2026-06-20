import threading
from conn.conn_socket import SocketConn
from scapy.contrib.bgp import BGPHeader
from conn.conn_handle import handle_open, handle_keepalive, handle_notification, handle_update


def get_open_bgp(conn):
    """
    Used for getting the first OPEN msg from client to confirm connectivity.
    """
    response = conn.recv()

    if not response:
        return None

    bgp = BGPHeader(response)
    handle_open(bgp)
    
    return response


def run_receiver(conn):

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
        print("[x] Something went wrong: ", e)


def receive_BGP(conn):
    while True:

        try:
            response = conn.recv()

            if not response:
                break

            bgp = BGPHeader(response)

            match bgp.type:
                case 1:
                    handle_open(bgp)
                case 2:
                    handle_update(bgp)
                case 3:
                    handle_notification(bgp)
                case 4:
                    handle_keepalive(bgp)
                case _:
                    print(f"\n[x] Received unknown bgp packet type")

        except ConnectionAbortedError as e:
            print(f"\n[x] Connection aborted: {e}")
            break

        except ConnectionResetError as e:
            print(f"\n[x] Connection reset: {e}")
            break

        except Exception as e:
            print(f"\n[x] Unexpected receive error: {e}")
            break