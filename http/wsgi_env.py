#!/usr/bin/python3
# a simple http service built directly against the low level wsgi spec.

from pprint import pformat
from wsgiref.simple_server import make_server


def app(environ, start_response):
    headers = {"Content-Type": 'text/plain; charset=utf-8'}
    start_response('200 OK', list(headers.items()))
    yield "Here is the WSGI environment:\r\n\r\n".encode('utf-8')
    yield pformat(environ).encode('utf-8')


if __name__ == '__main__':
    # httpd = make_server("", 8000, app)
    httpd = make_server("127.0.0.1", 8000, app)
    host, port = httpd.socket.getsockname()
    print("serving on", host, 'port', port)
    httpd.serve_forever()
