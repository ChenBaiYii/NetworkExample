#!/usr/bin/python3
# RPyC client

import rpyc


def main():
    config = {'allow_public_attrs': True}
    proxy = rpyc.connect('localhost', 18861, config=config)
    file_object = open("testfile.txt")
    line_count = proxy.root.line_counter(file_object, noisy)
    print('the number of lines in the file was', line_count)


def noisy(string):
    print("noisy:", repr(string))


if __name__ == '__main__':
    main()
