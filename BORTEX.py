import time
from scapy.all import *
from scapy.contrib.bgp import BGPHeader, BGPOpen
import socket

from misc.main_menu import main_menu


def main() -> None:
    """Entry point for the BGP tool CLI application

    Initializes runtime state by clearing previous session logs and routing
    database files, then launches the interactive command-line interface.

    The function runs an infinite loop that delegates control to the CLI
    handler (main_menu), effectively keeping the application alive until
    explicitly terminated via user command.
    """

    with open('./resources/profile.log', 'w') as f:
        pass
    
    with open('./resources/route.json', 'w') as f:
        pass
    
    print("\nWelcome to BORTEX\n[help] to see existing commands\n[exit] to exit")
    while True:
        action = main_menu()


if __name__ == "__main__":
    main()