# client that sends data then closes the socket, not expecting a reply

import socket
from argparse import ArgumentParser


def server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(address)
    sock.listen(1)
    print("run this script in another window with '-c' to connect")
    print("listening at", sock.getsockname())
    connect_sock, new_sock_name = sock.accept()
    print("accept connect from:", new_sock_name)
    connect_sock.shutdown(socket.SHUT_WR)
    message = b''
    while True:
        more = connect_sock.recv(8192)  # arbitrary value of 8k
        if not more:  # socket has closed when recv() returns ''
            print("received zero bytes - end of file")
            break
        print("received {} bytes".format(len(more)))
        message += more
    print("message:\n")
    print(message.decode('ascii'))
    connect_sock.close()
    sock.close()


def client(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.shutdown(socket.SHUT_RD)
    sock.sendall(b"beautiful is better than ugly.\n")
    sock.sendall(b"explicit is better than implicit.\n")
    sock.sendall(b"simple is better than complex.\n")
    sock.close()


if __name__ == '__main__':
    parser = ArgumentParser(description="transmit & receive a data stream")
    parser.add_argument("hostname", nargs="?", default="127.0.0.1", help="ip address or hostname default: %(default)s")
    parser.add_argument('-c', action="store_true", help="run as client")
    parser.add_argument('-p', type=int, metavar='port', default=1060, help="tcp port number default: %(default)s")
    args = parser.parse_args()
    run = client if args.c else server
    run((args.hostname, args.p))
