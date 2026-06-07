######################################################################
# 1. Create Open Msg & Update Msg
# 2. Create broadcast msg to understand entire network
# 3. Find a way to hijack (hijack what, and how)
# 4. Post Exploit
######################################################################

import time

from scapy.all import *
from scapy.contrib.bgp import BGPHeader, BGPOpen


from menu.menus import main_menu
import socket


def main():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((neighbor_ip, 179))

    print("Welcome to Black Girl Power (BGP)")
    while True:
        action = main_menu()


        


if __name__ == "__main__":
    main()