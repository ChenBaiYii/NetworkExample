#!/usr/bin/python3
# basic email

import email.message
import email.policy
import email.utils
import sys

text = """ hello, this is a basic message from chapter 12. - anonymous """


def main():
    message = email.message.EmailMessage(email.policy.SMTP)
    message['To'] = "recipient@example.com"
    message['From'] = "test sender <sender@example.com>"
    message['Subject'] = "test message, chapter 12"
    message['Date'] = email.utils.formatdate(localtime=True)
    message['Message-Id'] = email.utils.make_msgid()
    message.set_content(text)
    sys.stdout.buffer.write(message.as_bytes())


if __name__ == '__main__':
    main()
