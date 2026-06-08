import socket

class SocketConn:
    def __init__(self, target_ip:str, target_port:int):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((target_ip, target_port))

    def send(self, data):
        self.sock.send(data)

    def recv(self):
        return self.sock.recv(4096)

    def quit(self):
        self.sock.close()
