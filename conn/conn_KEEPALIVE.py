from scapy.contrib.bgp import BGPHeader
import threading
import time


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