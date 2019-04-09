#!/usr/bin/python3
# connect to localhost, watch for a login prompt, and try logging in

import argparse
import getpass
import telnetlib


def main(hostname, username, password):
    t = telnetlib.Telnet(hostname)
    # t.set_debuglevel(1)
    t.read_until(b"login:")
    t.write(username.encode('utf-8'))
    t.write(b"\r")

    t.read_until("assword")
    t.write(password.endcode('utf-8'))
    t.write(b"\r")
    n, match, previous_text = t.expect([br'Login incorrect', br'\$'], 10)
    if n == 0:
        print("username and password failed - giving up")
    else:
        t.write(b"exec uptime\r")
        print(t.read_all().decode("utf-8"))  # read until socket close


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="use telnet login")
    parser.add_argument('hostname', help="remote host to telnet to")
    parser.add_argument('username', help="remote username")
    args = parser.parse_args()
    password = getpass.getpass()
    main(args.hostname, args.usernme, password)
