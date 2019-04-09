# upd client and server for broadcast messages on a local lan
import argparse
import socket

MAX_BYTES = 65535


def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    while True:
        print("the server listening at {}".format(sock.getsockname()))
        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode("ascii")
        print("the client send at {} says {}".format(address, text))


def client(network, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    text = "broadcast datagram"
    data = text.encode("ascii")
    print("client send {}.".format(text))
    sock.sendto(data, (network, port))


if __name__ == "__main__":
    choice = {"server": server, "client": client}
    parser = argparse.ArgumentParser(description="send and receive udp broadcast")
    parser.add_argument("role", choices=choice, help="which role to take")
    parser.add_argument("host", help="interface listening at; network client sends to")
    parser.add_argument("-p", type=int, metavar="port", default=1060, help="udp prot (default port 1060)")
    args = parser.parse_args()
    run = choice[args.role]
    run(args.host, args.p)
