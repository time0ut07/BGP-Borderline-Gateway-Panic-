from conn.conn_OPEN import conn_OPEN
from conn.conn_KEEPALIVE import conn_KEEPALIVE
from misc.grab_settings import get_config
import threading


def conn_run():
    connOpen = conn_OPEN()

    if connOpen != None:

        with open("./resources/profile.log", "r") as f:
            for line in f:
                line = line.strip().split(": ")
                
                if line[0] == "Hold Time":
                    target_hold_time = int(line[1])
                    break

        our_hold_time = int(get_config(["hold_time"])["hold_time"])

        negotiated_hold_time = min(our_hold_time, target_hold_time) / 3

        thread = threading.Thread(
            target=conn_KEEPALIVE,
            args=(connOpen, negotiated_hold_time),
            daemon=True
        )

        thread.start()

    return None