#!/usr/bin/python3
# using ssh like telnet: connecting and running two commands

import sys
import argparse
import getpass
import paramiko


class AllowAnythingPolicy(paramiko.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return


def main(hostname, username):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(AllowAnythingPolicy())
    print("hsotname: {}, usrname: {}".format(hostname, username))
    client.connect(hostname, username=username, password=getpass.getpass())  # 登录
    channel = client.invoke_shell()
    stdin = channel.makefile('wb')
    stdout = channel.makefile('rb')

    stdin.write(b"echo hello, world\rexit\r")
    output = stdout.read()
    client.close()
    sys.stdout.buffer.write(output)
    print("over")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="connect over ssh")
    parser.add_argument('hostname', help="remote machine name")
    parser.add_argument('username', help='username on th remote machine')
    args = parser.parse_args()
    main(args.hostname, args.username)
