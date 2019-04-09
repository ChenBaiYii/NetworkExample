import argparse, socket
from datetime import datetime

MAX_BYTE = 65535


def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', port))

    print("listening at {}".format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(MAX_BYTE)
        text = data.decode("ascii")
        print("the client at {} says {!r}".format(address, text))
        text = "you data was {} byte long.".format(len(data))
        data = text.encode("ascii")
        sock.sendto(data, address)


def client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = "the time is {}".format(datetime.now())
    data = text.encode("ascii")
    sock.sendto(data, ('127.0.0.1', port))
    print("the os assigned me address {}".format(sock.getsockname()))
    data, address = sock.recvfrom(MAX_BYTE)
    text = data.decode("ascii")
    print("the server {} replied {!r}".format(address, text))


if __name__ == "__main__":
    choice = {"client": client, "server": server}
    parser = argparse.ArgumentParser(description="send and receive up locally")
    parser.add_argument("role", choices=choice, help="which role to play")
    parser.add_argument("-p", metavar='PORT', type=int, default=1060, help="upd port (default 1060)")
    args = parser.parse_args()
    run = choice[args.role]
    run(args.p)
