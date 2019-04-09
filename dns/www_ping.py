# find the www service of an aritrary host using getaddrinfo function

import argparse
import sys
import socket


def connect_to(hostname_or_ip):
    try:
        info_list = socket.getaddrinfo(
            hostname_or_ip, "www", 0, socket.SOCK_STREAM, 0,
            socket.AI_ADDRCONFIG | socket.AI_V4MAPPED | socket.AI_CANONNAME
        )
    except socket.gaierror as error:
        print("name service failure:", error.args[1])
        sys.exit(1)

    info = info_list[0]  # per standard recommendation, try first one
    socket_args = info[0:3]
    address = info[4]
    sock = socket.socket(*socket_args)
    try:
        sock.connect(address)
    except socket.error as error:
        print("network failure:", error.args[1])
    else:
        print("success: host", info[3], "is listening on port 80")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="try connect to port 80")
    parser.add_argument("hostname", help="hostname that you want to contact")
    args = parser.parse_args()
    connect_to(args.hostname)
