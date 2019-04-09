#!/usr/bin/python3
# small application that uses several different message queues

import random
import threading
import time
import zmq

B = 32  # number of bits of precision in each random integer


def ones_and_zeros(digits):
    """ express 'n' in at least 'd' binary digits, with no special prefix. """
    return bin(random.getrandbits(digits)).lstrip('ob').zfill(digits)


def bit_source(zcontext, url):
    """ produce random points in the unit square """
    zsock = zcontext.socket(zmq.PUB)  # zmp.PUB 是服务器类型
    zsock.bind(url)
    while True:
        zsock.send_string(ones_and_zeros(B * 2))
        time.sleep(0.1)


def always_yes(zcontext, in_url, out_url):
    """ coordinates in the lower-left quadrant are inside the unit circle. """
    isock = zcontext.socket(zmq.SUB)  # zmp.SUB 是客户端类型
    isock.connect(in_url)
    isock.setsockopt(zmq.SUBSCRIBE, b'00')  # 过滤条件 只有 00 开头的数据会被接受
    osock = zcontext.socket(zmq.PUSH)
    osock.connect(out_url)
    while True:
        isock.recv_string()
        osock.send_string("Y")


def judge(zcontext, in_url, pythagoras_url, out_url):
    """ determine whether each input coordinate is inside the unit circle """
    isock = zcontext.socket(zmq.SUB)
    isock.connect(in_url)
    for prefix in b'01', b'10', b'11':
        isock.setsockopt(zmq.SUBSCRIBE, prefix)  # 过滤条件 只有 prefix 开头的数据会被接受

    psock = zcontext.socket(zmq.REQ)    #
    psock.connect(pythagoras_url)
    osock = zcontext.socket(zmq.PUSH)
    osock.connect(out_url)
    unit = 2 ** (B * 2)
    while True:
        bits = isock.recv_string()
        n, m = int(bits[::2], 2), int(bits[1::2], 2)
        psock.send_json((n, m))
        sumsquares = psock.recv_json()
        osock.send_string('Y' if sumsquares < unit else 'N')


def pythagoras(zcontext, url):
    """ return the sum of squares of number sequences. """
    zsock = zcontext.socket(zmq.REP)
    zsock.bind(url)
    while True:
        numbers = zsock.recv_json()
        zsock.send_json(sum(n * n for n in numbers))


def tally(zcontext, url):
    """ tally how many points fall within the unit circle, and print pi. """
    zsock = zcontext.socket(zmq.PULL)
    zsock.bind(url)
    p = q = 0
    while True:
        decision = zsock.recv_string()
        q += 1
        if decision == 'Y':
            p += 4
        print(decision, p / q)


def start_thread(fun, *args):
    thread = threading.Thread(target=fun, args=args)
    thread.daemon = True  # so you can easily ctrl-c the whole program
    thread.start()


def main(zcontext):
    pub_sub = "tcp://127.0.0.1:6700"
    req_rep = "tcp://127.0.0.1:6701"
    push_pull = "tcp://127.0.0.1:6702"
    start_thread(bit_source, zcontext, pub_sub)
    start_thread(always_yes, zcontext, pub_sub, push_pull)
    start_thread(judge, zcontext, pub_sub, req_rep, push_pull)
    start_thread(pythagoras, zcontext, req_rep)
    start_thread(tally, zcontext, push_pull)
    time.sleep(30)


if __name__ == '__main__':
    main(zmq.Context())  # 返回一个套接字
