"""Functions to export"""

import socket

BUFFER_SIZE = 4096


def tee(source, destinations):
    """Mirror UDP traffic from source to destinations"""
    print(f"Listening on {source}")
    print(f"Forwarding to {destinations}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(source)

    while True:
        data, _ = sock.recvfrom(BUFFER_SIZE)
        for destination in destinations:
            sock.sendto(data, destination)
