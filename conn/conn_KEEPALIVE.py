from scapy.contrib.bgp import BGPHeader
import threading
import time

from misc.grab_config import get_config
from misc.logging import handle_log
from misc.status import get_status
from conn.conn_socket import SocketConn


def run_KEEPALIVE(conn:SocketConn) -> None:
    """Calculate the negotiated hold time interval and spawn the background heartbeat thread

    Reads the peer's hold time from a profile runtime file, compares it against the 
    local configuration to find the minimum value, divides it by three per RFC 4271 
    specifications, and starts a daemonised background thread

    Args:
        conn (SocketConn): The underlying active TCP control socket connecting the peer
    """
        
    # get holdtime
    with open("./resources/profile.log", "r") as f:
        for line in f:
            line = line.strip().split(": ")
            
            if line[0] == "Hold Time":
                target_hold_time = int(line[1])
                break

    # calculated hold time
    our_hold_time = int(get_config(["hold_time"])["hold_time"])
    negotiated_hold_time = min(our_hold_time, target_hold_time) / 3

    try:
        # run keepalive thread
        print("[*] Attempting to run KEEPALIVE in the background...")
        thread = threading.Thread(
            target=conn_KEEPALIVE,
            args=(conn, negotiated_hold_time),
            daemon=True
        )

        thread.start()
        print(f'[+] KEEPALIVE sending every {negotiated_hold_time}s')

    except Exception as e:
        print("[x] Something went wrong [run_KEEPALIVE]: ", e)


def conn_KEEPALIVE(conn:SocketConn, interval:float) -> None:
    """Execute the persistent loop sending BGP KEEPALIVE packets at a set interval

    Monitors the application connection matrix state loop. If active, it dispatches 
    raw BGP type-4 headers over the wire and sleeps. Automatically terminates if 
    the connection drops or a network socket write error encounters an exception

    Args:
        conn (SocketConn): The underlying active TCP control socket connecting the peer
        interval (float): The sleep time window in seconds between message dispatches
    """

    keepalive_pkt = BGPHeader(type=4)
    ip = get_config(["neighbor_ip"])["neighbor_ip"]

    while True:
        try:
            
            if get_status('bgp_connection') is True:
                conn.send(keepalive_pkt)
                print("\n[+] KEEPALIVE sent\n")
                handle_log(f"KEEPALIVE sent to {ip}", "bgp.log")
                time.sleep(interval)
            else:
                print("[x] BGP connection closed, stopping KEEPALIVE")
                break
            
        except Exception as e:
            print("[x] Something went wrong [conn_KEEPALIVE]:", e)
            break
