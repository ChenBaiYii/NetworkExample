#!/usr/bin/python3

import sys
import smtplib
import socket

message_template = """To: {}
From:{}
Subject: Test message from script

hello,
this is a test message.
"""


def main():
    if len(sys.argv) < 4:
        name = sys.argv[0]
        print("usage: {} server FromAddress ToAddress [ToAddress]".format(name))
        sys.exit(2)

    server, from_address, to_address = sys.argv[1], sys.argv[2], sys.argv[3:]
    message = message_template.format(', '.join(to_address), from_address)
    try:
        connection = smtplib.SMTP(server)
        connection.set_debuglevel(1)
        connection.sendmail(from_address, to_address, message)
    except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException) as e:
        print("you message may not have been sent!")
        print(e)
        sys.exit(1)
    else:
        s = '' if len(to_address) == 1 else 's'
        print("message sent to {} recipient{}".format(len(to_address), s))
        connection.quit()


if __name__ == '__main__':
    main()
