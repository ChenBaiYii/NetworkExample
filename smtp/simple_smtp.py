#!/usr/bin/python3

import sys
import smtplib

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
    connection = smtplib.SMTP(server)
    connection.sendmail(from_address, to_address, message)
    connection.quit()

    s = '' if len(to_address) == 1 else 's'
    print("message sent to {} recipient{}".format(len(to_address), s))
