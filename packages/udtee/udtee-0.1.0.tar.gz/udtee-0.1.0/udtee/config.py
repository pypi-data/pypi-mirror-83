"""Handles configuration parsing"""

import os
from argparse import ArgumentError
from urllib.parse import urlparse


def parse(source_arg, destinations_arg):
    """Parse configuration from CLI"""
    if source_arg:
        source_string = source_arg
    elif os.getenv("UDTEE_SOURCE"):
        source_string = os.getenv("UDTEE_SOURCE")
    else:
        raise ArgumentError

    if destinations_arg:
        destination_strings = destinations_arg.split(",")
    elif os.getenv("UDTEE_DESTINATIONS"):
        destination_strings = os.getenv("UDTEE_DESTINATIONS").split(",")
    else:
        raise ArgumentError

    source_address = split_host_and_port(source_string)
    destination_addresses = [split_host_and_port(d) for d in destination_strings]

    return source_address, destination_addresses


def split_host_and_port(address_string):
    """Parse address string into host and port"""
    url = urlparse(f"//{address_string}")
    if not url.port:
        raise ValueError
    return (url.hostname, url.port)
