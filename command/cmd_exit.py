import sys
from misc.status import change_status


def exit_app() -> None:
    """Gracefully terminate tool and change all status back to default

    Resets the internal system flags and notify the user about exiting
    """

    change_status('bgp_connection', 0)
    change_status('sniff', 0)
    change_status('routing', 0)

    print('[+] Exiting BORTEX gracefully...')

    sys.exit(1)