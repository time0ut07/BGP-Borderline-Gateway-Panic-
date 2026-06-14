from conn.conn_OPEN import conn_OPEN
from conn.conn_KEEPALIVE import conn_KEEPALIVE, run_KEEPALIVE
from conn.conn_receive import run_receiver


def conn_run(mode):

    if mode == "OPEN":
        connOpen = conn_OPEN()

        if connOpen is not None:

            run_KEEPALIVE(connOpen)
            run_receiver(connOpen)

        return connOpen

    elif mode == "UPDATE":
        print("UPDATEEEEEEEE ME")
        return None

    return None