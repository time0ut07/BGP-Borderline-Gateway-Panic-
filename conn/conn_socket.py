import socket
from scapy.all import raw


class SocketConn:
    """Lightweight wrapper around a TCP socket for BGP communication

    Encapsulates the underlying TCP socket used to establish, send, receive,
    and terminate a connection with a remote BGP peer. The class transparently
    handles both raw byte streams and Scapy packet objects when transmitting
    data.
    """

    def __init__(self, target_ip:str, target_port:int) -> None:
        """Create and establish a TCP connection to a remote peer

        Args:
            target_ip (str): IPv4 address of the remote BGP neighbor
            target_port (int): TCP port used by the remote BGP service
        """

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((target_ip, target_port))


    def send(self, data: bytes | object) -> None:
        """Transmit data through the established TCP connection

        Sends raw bytes directly or converts Scapy packet objects into their
        serialized byte representation before transmission

        Args:
            data (bytes | object): Raw byte stream or Scapy packet to send
        """

        if isinstance(data, bytes):
            self.sock.send(data)
        else:
            self.sock.send(raw(data))


    def recv(self, timeout: int | float = 10) -> bytes | None:
        """Receive data from the remote peer with a configurable timeout

        Waits for incoming data until the specified timeout expires

        Args:
            timeout (int | float): Maximum number of seconds to wait for
                incoming data before returning

        Returns:
            bytes | None: The received byte stream, or None if the receive
            operation times out
        """

        self.sock.settimeout(timeout)

        try:
            return self.sock.recv(4096)
        except socket.timeout:
            return None


    def quit(self):
        """Close the active TCP socket connection

        Releases the underlying network socket and terminates communication
        with the remote peer
        """

        self.sock.close()
