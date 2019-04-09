#!/usr/bin/python3

import sys
import imaplib
import getpass


def main():
    if len(sys.argv) != 3:
        print("usage: %s hostname username" % sys.argv[0])
        sys.exit(2)

    hostname, username = sys.argv[1:]
    m = imaplib.IMAP4_SSL(hostname)
    m.login(username, getpass.getpass())
    try:
        print("capabilities:", m.capabilities)
        print("listing mailboxes ")
        status, data = m.list()
        print("status:", repr(status))
        print("data:")
        for datum in data:
            print(repr(datum))
    finally:
        m.logout()


if __name__ == '__main__':
    main()
