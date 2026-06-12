from conn.conn_OPEN import conn_OPEN
from conn.conn_KEEPALIVE import conn_KEEPALIVE, run_KEEPALIVE


def conn_run(mode):

    if mode == "OPEN":
        connOpen = conn_OPEN()

        if connOpen != None:

            run_KEEPALIVE(connOpen)

        return None

    else:
        print("UPDATEEEEEEEE ME")
        return None