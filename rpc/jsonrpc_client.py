#!/usr/bin/python3
# json rpc client needing "pip install jsonrpclib-pelix"

from jsonrpclib import Server


def main():
    proxy = Server("http://localhost:7002")
    print(proxy.lengths((1, 2, 3), 27, {'sirius': -1.46, 'rigel': 0.12}))


if __name__ == '__main__':
    main()
