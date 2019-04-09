#!/usr/bin/python3
# opening an internet mail access protocol connection with the powerful IMAPClient

import sys
import getpass
from imapclient import IMAPClient


def main():
    if len(sys.argv) != 3:
        print("usage: %s hostname username" % sys.argv[0])
        sys.exit(2)
    hostname, username = sys.argv[1:]
    c = IMAPClient(hostname, ssl=True)
    try:
        c.login(username, getpass.getpass())
    except c.Error as e:
        print("could not log in:", e)
    else:
        print('capabilities:', c.capabilities())
        print("listing mailboxes:")
        data = c.list_folders()
        for flags, delimiter, folder_name in data:
            print('%-30s%s %s' % (' '.join(flags), delimiter, folder_name))
    finally:
        c.logout()


if __name__ == '__main__':
    main()
