# sending data over a stream but delimited as length-prefixed blocks

import socket, struct
from argparse import ArgumentParser

header_struct = struct.Struct('!I')  # message up to 2**32 - 1 in length


def receive_all(sock, length):
    blocks = []
    while length:
        block = sock.recv(length)
        if not block:
            raise EOFError("socket closed with %d bytes left in this block".format(length))
        length -= len(block)
        blocks.append(block)
    return b''.join(blocks)


def get_block(sock):
    data = receive_all(sock, header_struct.size)
    (block_length,) = header_struct.unpack(data)
    return receive_all(sock, block_length)


def server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(1)
    print("run this script in another window with '-c' to connect")
    print("listening at", sock.getsockname())
    connect_sock, new_sock_name = sock.accept()
    print("accepted connect from", new_sock_name)
    connect_sock.shutdown(socket.SHUT_WR)
    while True:
        block = get_block(connect_sock)
        if not block:
            break
        print("block says:", repr(block))
    connect_sock.close()
    sock.close()


def put_block(sock, message):
    block_length = len(message)
    sock.send(header_struct.pack(block_length))
    sock.send(message)


def client(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.shutdown(socket.SHUT_RD)
    put_block(sock, b"beautiful is better than ugly.")
    put_block(sock, b"explicit is better than implicit.")
    put_block(sock, b"simple is better than complex.")
    put_block(sock, b"")
    sock.close()


if __name__ == '__main__':
    parser = ArgumentParser(description="transmit & receive blocks over tcp")
    parser.add_argument('hostname', nargs="?", default="127.0.0.1", help="ip address or hostname default: %(default)s")
    parser.add_argument('-c', action="store_true", help="run as client")
    parser.add_argument('-p', type=int, metavar='port', default=1060, help="tcp port number default: %(default)s")
    args = parser.parse_args()
    run = client if args.c else server
    run((args.hostname, args.p))
