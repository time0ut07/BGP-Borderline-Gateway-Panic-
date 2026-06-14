from scapy.contrib.bgp import BGPHeader
import threading
import time
from misc.grab_settings import get_config
from misc.logging import handle_log


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
        print("[*] Attempting to run KEEPALIVE in the background...")
        thread = threading.Thread(
            target=conn_KEEPALIVE,
            args=(conn, negotiated_hold_time),
            daemon=True
        )

        thread.start()
        print(f'[+] KEEPALIVE sending every {negotiated_hold_time}s')

    except Exception as e:
        print("[x] Something went wrong: ", e)

    return 0


def conn_KEEPALIVE(conn, interval):
    keepalive_pkt = BGPHeader(type=4)
    ip = get_config(["neighbor_ip"])["neighbor_ip"]

    while True:
        try:
            conn.send(keepalive_pkt)
            print("\n[+] KEEPALIVE sent\n")
            handle_log(f"KEEPALIVE sent to {ip}")
            time.sleep(interval)
        except Exception as e:
            print("\n[-] KEEPALIVE failed:", e)
            break