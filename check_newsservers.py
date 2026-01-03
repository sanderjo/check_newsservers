newsserver = "news.newshosting.com"
port = 563

# check if newsserver has an IPv4 address
import socket
try:
    socket.inet_pton(socket.AF_INET, newsserver)
    has_ipv4 = True
except socket.error:
    has_ipv4 = False

# check if newsserver has an IPv6 address
try:
    socket.inet_pton(socket.AF_INET6, newsserver)
    has_ipv6 = True
except socket.error:
    has_ipv6 = False


# check if we can connect to the newsserver on the specified port, and get the connection message

import socket
def can_connect(host, port):
    try:
        with socket.create_connection((host, port), timeout=5):
            return True
    except (socket.timeout, socket.error):
        return False

can_connect_result = can_connect(newsserver, port)
connection_message = ""
if can_connect_result:
    connection_message = f"Successfully connected to {newsserver} on port {port}."
else:
    connection_message = f"Failed to connect to {newsserver} on port {port}."
print(connection_message)

# connect to the newsserver via SSL/TLS and get the server's greeting message

import ssl
def get_greeting_message(host, port):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                greeting = ssock.recv(1024).decode('utf-8')
                return greeting.strip()
    except (socket.timeout, socket.error, ssl.SSLError):
        return "Could not retrieve greeting message."

greeting_message = get_greeting_message(newsserver, port)
print(f"Greeting message from server: {greeting_message}")