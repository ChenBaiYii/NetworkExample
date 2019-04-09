#!/usr/bin/python3
# json rpc server needing "pip install jsonrpclib-pelix"


from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer


def lengths(*args):
    """ measure the length of each input argument.
    given N argument, this function returns a list of N smaller lists of the
    form [len(arg), arg] that each state the length of an input argument and
    also echo back the argument itself.
    """
    results = []
    for arg in args:
        try:
            arg_len = len(arg)
        except TypeError as e:
            arg_len = None
        results.append((arg_len, arg))
    return results


def main():
    server = SimpleJSONRPCServer(('localhost', 7002))
    server.register_function(lengths)
    print('starting server')
    server.serve_forever()


if __name__ == '__main__':
    main()
