import threading
from conn.conn_socket import SocketConn
from scapy.contrib.bgp import BGPHeader
from conn.conn_handle import handle_keepalive, handle_notification, handle_update


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
        response = conn.recv()

        if not response:
            break

        bgp = BGPHeader(response)

        if bgp.type == 2:
            handle_update(bgp)

        elif bgp.type == 4:
            handle_keepalive(bgp)

        elif bgp.type == 3:
            handle_notification(bgp)