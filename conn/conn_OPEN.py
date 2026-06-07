# open from peer
# keepalive exchange (multithread?) to mainatin sess

from scapy.contrib.bgp import *
from tabulate import tabulate
from socket import socket


def conn_OPEN():

    configs = ["version", "asn", "hold_time", "bgp_id", "local_ip"]
    settings = {}

    with open("./resources/settings.txt", 'r') as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue
            
            key, value = line.split("=", 1)
            settings[key.strip()] = value.strip()

    open_msg_table = [
        ["version", settings["version"]],
        ["my_as", settings["asn"]],
        ["hold_time", settings["hold_time"]],
        ["bgp_id", settings["bgp_id"]],
    ]

    print(tabulate(open_msg_table, headers=["Field", "Value"], tablefmt="grid"))

    while True:
        send = (input("\n[*] Send BGP OPEN Packet (y/n): ")).lower()

        match send:
            case 'y':
                break
            case 'n':
                print("[x] Cancelling operation...\n")
                return 0
            case _:
                print("[x] Invalid option")

    open_msg = BGPOpen(
        version=int(settings["version"]),
        my_as=int(settings["asn"]),
        hold_time=int(settings["hold_time"]),
        bgp_id=str(settings["bgp_id"])
    )

    pkt = BGPHeader(type=1) / open_msg
    raw_bgp = raw(pkt)

    print("[+] BGP OPEN packet built...")


    return "XXXXXX"


def send_bgp_OPEN(session, raw_bgp):
    ip = session["ip"]

    tcp = TCP(
        sport=session["sport"],
        dport=session["dport"],
        flags="PA",
        seq=session["seq"],
        ack=session["ack"]
    )

    resp = sr1(ip/tcp/raw_bgp, timeout=3)

    session["seq"] += len(raw_bgp)

    if resp:
        session["ack"] = resp.seq + len(resp[Raw].load) if Raw in resp else session["ack"]

    return session, resp