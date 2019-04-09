#!/usr/bin/python3
# running two remote commands simultaneously in different channels

import argparse
import threading
import getpass
import paramiko


class AllowAnythingPolicy(paramiko.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return


def main(hostname, username):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(AllowAnythingPolicy())
    print("hostname: {}, username: {}".format(hostname, username))
    client.connect(hostname, username=username, password=getpass.getpass())

    def read_unitl_EOF(file_object):
        s = file_object.readline()
        while s:
            print(s.strip())
            s = file_object.readline()

    ioe1 = client.exec_command("echo One;sleep 2;echo Two;sleep 1;echo Three")
    ioe2 = client.exec_command("echo A;sleep 1;echo B;sleep 2;echo C")

    thread_1 = threading.Thread(target=read_unitl_EOF, args=(ioe1[1],))
    thread_2 = threading.Thread(target=read_unitl_EOF, args=(ioe2[1],))

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

    client.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="connect over ssh")
    parser.add_argument('hostname', help="remote machine name")
    parser.add_argument('username', help='username on th remote machine')
    args = parser.parse_args()
    main(args.hostname, args.username)
