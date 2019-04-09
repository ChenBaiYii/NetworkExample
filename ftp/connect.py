#!/usr/bin/python3
# simple ftp example

from ftplib import FTP


def main():
    ftp = FTP('ftp.ibiblio.org')
    print("welcome:", ftp.getwelcome())
    ftp.login()
    ftp.quit()


if __name__ == "__main__":
    main()
