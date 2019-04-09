# constants and routines for a certain network conversation

import argparse
import socket
import time

aphorisms = {b"beautiful is better than?": b"ugly.",
             b"explicit is better than?": b"implicit.",
             b"simple is better than?": b"complex"}


def get_answer(aphorism):
    """ return the string response to a particular zen of python aphorism. """
    time.sleep(0.0)  # increase to simulate an expensive operation
    return aphorisms.get(aphorism, b"error: unknown aphorism")


def parse_command_line(description):
    """ parse command line and return a socket address """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("host", help="ip or hostname")
    parser.add_argument('-p', metavar='port', type=int, default=1060, help="tcp port default %(default)s")
    args = parser.parse_args()
    address = (args.host, args.p)
    return address


def create_srv_socket(address):
    """ build an return a listening server socket """
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(address)
    listener.listen(64)
    print("listening at {}".format(address))
    return listener


def accept_connections_forever(listener):
    """ forever answer incoming connections on a listening socket """
    while True:
        connect_sock, new_sock_name = listener.accept()
        print("accepted connection from {}".format(new_sock_name))
        handler_conversation(connect_sock, new_sock_name)


def handler_conversation(sock, address):
    """ converse with a client or over 'sock' until they are done talking """
    try:
        while True:
            handler_request(sock)
    except EOFError:
        print("client socket to {} has closed.".format(address))
    except Exception as e:
        print("debug ----------------")
        print("client {} error: {}".format(address, e))
    finally:
        sock.close()


def handler_request(sock):
    """ receive a single client request on 'sock' and send the answer """
    aphorism = receive_until(sock, b"?")
    answer = get_answer(aphorism)
    sock.sendall(answer)
    print("send message:", answer)
    print("clear")


def receive_until(sock, suffix):
    """ receive bytes over socket 'sock' until we receive th 'suffix'. """
    message = sock.recv(4096)
    if not message:
        raise EOFError("socket closed")
    while not message.endswith(suffix):
        data = sock.recv(4096)
        if not data:
            raise IOError("received {!r} then socket closed".format(message))
        message += data
    return message
