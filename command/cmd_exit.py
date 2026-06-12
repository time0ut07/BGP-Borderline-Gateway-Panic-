import sys


def exit_app():
    print('[+] Exiting BGP Tool Name gracefully...')

    with open('./resources/profile.log', 'w') as f:
        pass

    print('byebye :)')
    sys.exit(1)