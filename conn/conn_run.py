from conn.conn_OPEN import conn_OPEN
from conn.conn_KEEPALIVE import conn_KEEPALIVE, run_KEEPALIVE
from conn.conn_UPDATE import send_UPDATE
from conn.conn_receive import run_receiver
from conn.parse_BGP import get_connectivity


def conn_run(mode, connection=None):

    if mode == "OPEN":
        connection = conn_OPEN()

        if connection is not None:

            run_KEEPALIVE(connection)
            run_receiver(connection)

        return connection

    elif mode == "UPDATE": 

        if connection is None:
            print("[-] No active connection...")
            return None

        send_UPDATE(connection)

        return connection

    return connection