#!/usr/bin/python3
# running three separate commands, and reading htree separate outputs

import argparse
import paramiko
import getpass


class AllowAnythingPolicy(paramiko.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return


def main(hostname, username):
    client = paramiko.SSHClient()  # 初始化一个ssh客户端
    client.set_missing_host_key_policy(AllowAnythingPolicy())
    client.connect(hostname, username=username, password=getpass.getpass())  # password
    for command in 'echo "hello, wold!"', 'uname', 'uptime':
        stdin, stdout, stderr = client.exec_command(command)  # 执行命令
        stdin.close()
        print(repr(stdout.read()))
        stdout.close()
        stderr.close()

    client.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="connect over ssh")
    parser.add_argument('hostname', help="remote machine name")
    parser.add_argument('username', help='username on th remote machine')
    args = parser.parse_args()
    main(args.hostname, args.username)
