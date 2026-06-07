import socket

# to do make neighbour_ip dynamic and port
class SocketConn:
    def __init__(self, neighbor_ip):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((neighbor_ip, 179))

    def send(self, data):
        self.sock.send(data)

    def recv(self):
        return self.sock.recv(4096)

    def quit(self):
        self.sock.close()