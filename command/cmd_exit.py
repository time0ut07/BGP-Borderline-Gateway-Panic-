import sys
from misc.status import change_status


def exit_app():
    change_status('bgp_connection', 0)
    change_status('sniff', 0)
    change_status('routing', 0)
    print('[+] Exiting BGP Tool Name gracefully...')
    print('byebye :)')
    sys.exit(1)