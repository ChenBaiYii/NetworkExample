#!/usr/bin/python3
# xml rpc server

import operator
import math
from functools import reduce
from xmlrpc.server import SimpleXMLRPCServer


def main():
    server = SimpleXMLRPCServer(('127.0.0.1', 7001))
    server.register_introspection_functions()
    server.register_multicall_functions()
    server.register_function(add_together)
    server.register_function(quadratic)
    server.register_function(remote_repr)
    print("server ready")
    server.serve_forever()


def add_together(*things):
    """ add together everything in the list 'things'. """
    return reduce(operator.add, things)


def quadratic(a, b, c):
    """ determine 'x' value satisfying: 'a' * x*x + 'b' * x + c = 0 """
    b24ac = math.sqrt(b * b - 4.0 * a * c)
    return list(set([(-b - b24ac) / 2.0 * a, (-b + b24ac) / 2.0 * a]))


def remote_repr(arg):
    """ return th 'repr()' rendering of the supplied 'arg'. """
    return arg


if __name__ == '__main__':
    main()
