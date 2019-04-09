#!/usr/bin/python3
# characters are special (except that whitespace separates arguments)

import subprocess
from pipes import quote


def main():
    while True:
        args = input("$ ").strip().split()
        if not args:
            pass
        elif args[0] == "exit":
            break
        elif args[0] == "show":
            print("arguments:", args[1:])
        else:
            try:
                subprocess.call(args)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    main()
