# upd and server for talking over the network

import argparse
import random
import socket

MAX_BYTES = 65535


def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print("listening at {}".format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        if random.random < 0.5:
            print("drop")
            print("pretending to drop packet from {}".format(address))
            continue
        text = data.decode("ascii")
        print("the client as {} says {!r}".format(address, text))
        message = "you data was {} bytes long".format(len(data))
        sock.sendto(message.encode("ascii"), address)


def client(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # hostname = sys.argv[2]
    sock.connect((hostname, port))
    print("client socket name is {}.".format(sock.getsockname()))

    delay = 0.1  # seconds
    text = "this is another message"
    data = text.encode("ascii")

    while True:
        sock.send(data)
        print("waiting up to {} seconds for a replay".format(delay))
        sock.settimeout(delay)
        try:
            data = sock.recv(MAX_BYTES)
        except socket.timeout:
            delay *= 2  
            if delay > 2.0:
                raise RuntimeError("i think server is down")
        else:
            break  # done
    print("the server says {!r}".format(data.decode("ascii")))


if __name__ == '__main__':
    choice = {"client": client, "server": server}
    parser = argparse.ArgumentParser("send and receive upd, pretending packets are often dropped")
    parser.add_argument('role', choices=choice, help="which role a take")
    parser.add_argument('host', help="interface the server listening at; host the client send to")
    parser.add_argument('-p', metavar="PORT", type=int, default=1060, help="upd port (default 1060)")
    args = parser.parse_args()
    run = choice[args.role]
    run(args.host, args.p)
