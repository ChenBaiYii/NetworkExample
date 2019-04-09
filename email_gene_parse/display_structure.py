#!/usr/bin/python3

import argparse
import email.policy
import sys


def walk(part, prefix=''):
    yield prefix, part
    for i, subpart in enumerate(part.iter_parts()):
        yield from walk(subpart, prefix + '.{}'.format(i))


def main(binary_file):
    policy = email.policy.SMTP
    message = email.message_from_binary_file(binary_file, policy=policy)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="display MIME structure")
    parser.add_argument("filename", nargs='?', help="file containing an email")
    args = parser.parse_args()
    if args.filename is None:
        main(sys.stdin.buffer)  # 如果没有指定 filename 则从缓冲区读取数据
    else:
        with open(args.filename, 'rb') as f:
            main(f)  # 从文件读取
