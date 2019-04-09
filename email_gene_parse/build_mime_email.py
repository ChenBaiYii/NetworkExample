#!/usr/bin/python3
# mime email

import sys
import argparse
import email.message
import email.policy
import email.utils
import mimetypes

plain = """ hello, this is a basic message from chapter 12. - anonymous """

html = """<p>hello,</p>
<p> this is a <b>test message</b>  from chapter 12. </p>
 """

img = """ <p>this is the smallest possible blue GIF:</p>
<img src="cid:{}" height="80" width="80"> """

# tiny example GIF from http://www.perlmonks.org/?node_id=7974
blue_dot = (b'GIF89a1010\x900000\xff000,000010100\x02\x02\x0410;'.replace(b'0', b'\x00').replace(b'1', b'\x01'))


def main(args):
    message = email.message.EmailMessage(email.policy.SMTP)

    message['To'] = "recipient@example.com"
    message['From'] = "test sender <sender@example.com>"
    message['Subject'] = "foundations of python network programing"
    message['Date'] = email.utils.formatdate(localtime=True)
    message['Message-Id'] = email.utils.make_msgid()

    if not args.i:
        message.set_content(html, subtype="html")  # 设置消息主体
        message.add_alternative(plain)  # 该方法用于提供其他格式的电子邮件
    else:
        cid = email.utils.make_msgid()  # rfc 2392: must be globally unique!
        message.set_content(html + img.format(cid.strip('<>')), subtype='html')
        message.add_related(blue_dot, 'image', 'gif', cid=cid, filename='blue-dot.gif')  # 添加生成主体消息要用的其他资源
        message.add_alternative(plain)

    for filename in args.filename:
        mime_type, encoding = mimetypes.guess_type(filename)
        if encoding or (mime_type is None):
            mime_type = 'application/octet-stream'
        main, sub = mime_type.split('/')
        if main == 'text':
            with open(filename, encoding='utf-8') as f:
                text = f.read()
            message.add_attachment(text, sub, filename=filename)
        else:
            with open(filename, 'rb') as f:
                data = f.read()
            message.add_attachment(data, main, sub, filename=filename)
    sys.stdout.buffer.write(message.as_bytes())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="build, print mime email")
    parser.add_argument('-i', action="store_true", help="include gif image")
    parser.add_argument('filename', nargs='*', help="attachment filename")
    main(parser.parse_args())
