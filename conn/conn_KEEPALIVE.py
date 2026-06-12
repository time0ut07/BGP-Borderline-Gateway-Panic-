from scapy.contrib.bgp import BGPHeader
import threading
import time
from misc.grab_settings import get_config


def run_KEEPALIVE(conn):

    with open("./resources/profile.log", "r") as f:
        for line in f:
            line = line.strip().split(": ")
            
            if line[0] == "Hold Time":
                target_hold_time = int(line[1])
                break

    our_hold_time = int(get_config(["hold_time"])["hold_time"])
    negotiated_hold_time = min(our_hold_time, target_hold_time) / 3

    try:
        print("[+] Attempting to run KEEPALIVE in the background...")
        thread = threading.Thread(
            target=conn_KEEPALIVE,
            args=(conn, negotiated_hold_time),
            daemon=True
        )

        thread.start()

    except Exception as e:
        print("[x] Something went wrong: ", e)

    return 0


def conn_KEEPALIVE(conn, interval):
    keepalive_pkt = BGPHeader(type=4)

    while True:
        try:
            conn.send(keepalive_pkt)
            print("\n[+] KEEPALIVE sent\n")
            time.sleep(interval)
        except Exception as e:
            print("\n[-] KEEPALIVE failed:", e)
            break