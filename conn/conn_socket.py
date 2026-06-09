import socket
from scapy.all import raw


class SocketConn:
    """
    Socket Connection Things
    """
    def __init__(self, target_ip:str, target_port:int):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((target_ip, target_port))

    def send(self, data):
        if isinstance(data, bytes):
            self.sock.send(data)
        else:
            self.sock.send(raw(data))

    def recv(self, timeout=10):
        self.sock.settimeout(timeout)

        try:
            return self.sock.recv(4096)
        except socket.timeout:
            return None

    def quit(self):
        self.sock.close()
