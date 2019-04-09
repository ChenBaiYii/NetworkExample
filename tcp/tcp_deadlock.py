# tcp client and server that leave too much data waiting

import argparse
import socket
import sys


def server(host, port, byte_count):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)
    print("start listen")
    while True:
        connect_sock, sock_name = sock.accept()
        print("processing up to 1024 bytes at a time from ", sock_name)
        n = 0
        while True:
            data = connect_sock.recv(1024)
            if not data:
                break
            output = data.decode("ascii").upper().encode('ascii')
            connect_sock.sendall(output)
            n += len(data)
            print("\r %d bytes processed so far" % (n,), end='')
            sys.stdout.flush()
        print()
        connect_sock.close()
        print(" socket closed")


def client(host, port, byte_count):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    byte_count = (byte_count + 15)
    message = b"capitalize this"
    print("sending", byte_count, "bytes of data, in chunks of 16 bytes")
    sent = 0
    while sent < byte_count:
        sock.sendall(message)
        sent += len(message)
        print("\r %d bytes sent " % (sent,), end="")
        sys.stdout.flush()
    print()
    sock.shutdown(socket.SHUT_WR)
    print("receiving all the data the server sends back")

    received = 0
    while True:
        data = sock.recv(42)
        if not received:
            print("the first data received says", repr(data))
        if not data:
            break
        received += len(data)
        print("\r %d bytes received" % (received,), end=" ")
    print()
    sock.close()


if __name__ == '__main__':
    choice = {"server": server, "client": client}
    parser = argparse.ArgumentParser(description="get deadlocked over tcp")
    parser.add_argument("role", choices=choice, help="which role to play")
    parser.add_argument("host", help="interface the server listens at; host client sends to")
    parser.add_argument("byte_count", type=int, nargs="?", default=16,
                        help="number of bytes for client to send (default 16)")
    parser.add_argument("-p", metavar="PORT", type=int, default=1060, help="tcp port (default 1060)")
    args = parser.parse_args()
    run = choice[args.role]
    run(args.host, args.p, args.byte_count)
    # print(args.host, args.p, args.byte_count)
