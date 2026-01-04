newsserver = "news.newshosting.com"
newsserver = "news.eweka.nl"
newsserver = "news.stingyusenet.com"

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
def get_greeting_message_and_tls(host, port):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                ssock.settimeout(5)
                try:
                    greeting = ssock.recv(1024).decode('utf-8', errors='replace').strip()
                except (socket.timeout, socket.error):
                    greeting = ""
                tls_version = ssock.version()

                # after greeting is received, send CAPABILITIES and read until ".\r\n"
                capline = ""
                if greeting:
                    try:
                        # use a file-like wrapper to read line-by-line
                        fileobj = ssock.makefile('rwb')
                        fileobj.write(b"CAPABILITIES\r\n")
                        fileobj.flush()
                        capabilities = []
                        while True:
                            line = fileobj.readline()
                            if not line:
                                break
                            capabilities.append(line.decode('utf-8', errors='replace').rstrip('\r\n'))
                            if line == b".\r\n":
                                capline = ''.join(capabilities)
                                # print("Received CAPABILITIES response:")
                                for cap in capabilities:
                                    if cap.startswith('VERSION'):
                                        capline = cap
                                        break
                                break
                        # capabilities list is available here if needed
                    except (socket.timeout, socket.error, ssl.SSLError):
                        pass

                return greeting, tls_version, capline
    except (socket.timeout, socket.error, ssl.SSLError):
        return "Could not retrieve greeting message.", None

greeting_message, tls_version, capline = get_greeting_message_and_tls(newsserver, port)
print(f"Greeting message from server: {greeting_message}")
if tls_version:
    print(f"TLS version: {tls_version}")
else:
    print("TLS version: unknown")
if capline:
    print(f"CAPABILITIES line: {capline}")

# find all IPv4 and IPv6 addresses for the newsserver
def get_all_addresses(host):
    addresses = {'IPv4': [], 'IPv6': []}
    try:
        for res in socket.getaddrinfo(host, None):
            af, socktype, proto, canonname, sa = res
            if af == socket.AF_INET:
                addresses['IPv4'].append(sa[0])
            elif af == socket.AF_INET6:
                addresses['IPv6'].append(sa[0])
    except socket.gaierror:
        pass
    return addresses
all_addresses = get_all_addresses(newsserver)
print(f"All IPv4 addresses: {all_addresses['IPv4']}")
print(f"All IPv6 addresses: {all_addresses['IPv6']}")

# of all ipv4 addresses, find the unique /24 subnets
def get_unique_ipv4_subnets(ipv4_addresses):
    subnets = set()
    for ip in ipv4_addresses:
        parts = ip.split('.')
        if len(parts) == 4:
            subnet = '.'.join(parts[:3]) + '.0/24'
            subnets.add(subnet)
    return list(subnets)
unique_ipv4_subnets = get_unique_ipv4_subnets(all_addresses['IPv4'])
print(f"Unique /24 IPv4 subnets: {unique_ipv4_subnets}")

# of all ipv6 addresses, find the unique /48 subnets
def get_unique_ipv6_subnets(ipv6_addresses):
    subnets = set()
    for ip in ipv6_addresses:
        parts = ip.split(':')
        if len(parts) >= 3:
            subnet = ':'.join(parts[:3]) + '::/48'
            subnets.add(subnet)
    return list(subnets)
unique_ipv6_subnets = get_unique_ipv6_subnets(all_addresses['IPv6'])
print(f"Unique /48 IPv6 subnets: {unique_ipv6_subnets}")
