from scapy.contrib.bgp import BGPHeader, BGPUpdate
from scapy.all import *
import threading


def receive_UPDATE(conn):
    while True:
        data = conn.recv(4096)

        if not data:
            break


def thread_UPDATE():

    thread = threading.Thread(
        target=receive_UPDATE,
        args=(conn,),
        daemon=True
    )

    thread.start()


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


def send_update(conn):
    