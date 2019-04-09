# simple tcp client and server that send and receive sixteen octets
import argparse
import socket


def receive_all(sock, length):
    data = b""
    while len(data) < length:
        more = sock.recv((length - len(data)))
        if not more:
            raise EOFError(
                "was expecting %d bytes but only received %d bytes before the socket closed" % (length, len(data)))
        data += more
    return data


def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print("listening at {}".format(sock.getsockname()))
    while True:
        connected_sock, new_sock_name = sock.accept()
        print("we have accepted a connection from {}".format(new_sock_name))
        print(" socket name: {}".format(connected_sock.getsockname()))
        print(" socket peer: {}".format(connected_sock.getpeername()))
        message = receive_all(connected_sock, 16)
        print(" incoming sixteen-octet message:", repr(message))
        connected_sock.sendall(b"farewell, client!")
        connected_sock.close()
        print(" reply sent, socket closed")


def client(host, port):
    print("the arg port is : {}".format(port))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("client has been assigned socket name: ", sock.getsockname())
    sock.sendall(b"hi there, server")
    reply = receive_all(sock, 16)
    print("the serve said ", repr(reply))
    sock.close()


if __name__ == '__main__':
    choice = {"server": server, "client": client}
    parser = argparse.ArgumentParser(description="send and receive over tcp")
    parser.add_argument("role", choices=choice, help="which role to play")
    parser.add_argument("host", help="interface the server listens at; host the client sends to")
    parser.add_argument('-p', metavar="PORT", type=int, default=1060, help="tcp port (default 1060)")
    args = parser.parse_args()
    run = choice[args.role]
    run(args.host, args.p)
