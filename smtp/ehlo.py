#!/usr/bin/python3

import smtplib
import socket
import sys

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
        report_on_message_size(connection, from_address, to_address, message)
    except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException) as e:
        print("you message may not have been sent!")
        print(e)
        sys.exit(1)
    else:
        s = '' if len(to_address) == 1 else 's'
        print("message sent to {} recipient{}".format(len(to_address), s))
        connection.quit()


def report_on_message_size(connection, from_address, to_address, message):
    code = connection.ehlo()[0]
    uses_esmtp = (200 <= code <= 299)
    if not uses_esmtp:
        code = connection.helo()[0]
        if not (200 <= code <= 299):
            print('message too large; aborting.')
            sys.exit(1)

    if uses_esmtp and connection.has_extn('size'):
        print("maximum message size is", connection.esmtp_features['size'])
        if len(message) > int(connection.esmtp_features['size']):
            print("message too large; aborting.")
            sys.exit(1)
    connection.sendmail(from_address, to_address, message)


if __name__ == '__main__':
    main()
