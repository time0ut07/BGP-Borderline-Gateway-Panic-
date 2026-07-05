from misc.status import get_status, change_status
from conn.conn_OPEN import conn_OPEN
from conn.conn_KEEPALIVE import conn_KEEPALIVE, run_KEEPALIVE
from conn.conn_UPDATE import send_UPDATE
from conn.conn_receive import run_receiver
from conn.conn_socket import SocketConn
from pe.pe_sniffer import run_sniffer

def conn_run(mode: str, connection: SocketConn | None = None) -> SocketConn | None:
    """Dispatch and execute BGP connection operations based on the requested mode

    Routes execution to the appropriate connection handler. Depending on the
    selected mode, this function establishes a new BGP session, starts the
    KEEPALIVE and packet receiver threads, or sends a BGP UPDATE message using
    an existing active connection.

    Args:
        mode (str): The requested connection operation. Supported values are
            "OPEN" and "UPDATE".
        connection (SocketConn | None): An existing active BGP connection.
            Required for UPDATE operations and ignored when establishing a new
            connection.

    Returns:
        SocketConn | None: The active connection object after the requested
            operation completes, or None if the operation fails or no active
            connection exists.
    """

    if mode == "OPEN":
        connection = conn_OPEN()

        if connection is not None and get_status('bgp_connection') is True:

            run_KEEPALIVE(connection)
            run_receiver(connection)

        return connection

    elif mode == "UPDATE": 
        if connection is None or get_status('bgp_connection') is not True:
            print("[-] No active connection...")
            return None

        send_UPDATE(connection)

        return connection

    return connection
