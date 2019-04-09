#!/usr/bin/python3
# RPyC server

import rpyc


def main():
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MyService, port=18861)
    t.start()


class MyService(rpyc.Service):
    def exposed_line_counter(self, file_obj, func):
        print("client has invoked exposed_line_counter()")
        for line_num, line in enumerate(file_obj.readlines()):
            func(line)
        return line_num + 1


if __name__ == '__main__':
    main()
