######################################################################
# 1. Create Open Msg & Update Msg
# 2. Create broadcast msg to understand entire network
# 3. Find a way to hijack (hijack what, and how)
# 4. Post Exploit
######################################################################

# Things to do
# exit thread when exit 

import time

from scapy.all import *
from scapy.contrib.bgp import BGPHeader, BGPOpen


from misc.main_menu import main_menu
import socket


def main():
    
    print("\nWelcome to BGP Tool Name\n[help] to see existing commands\n[exit | quit] to exit")
    while True:
        action = main_menu()


if __name__ == "__main__":
    main()