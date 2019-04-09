# uses the legacy "socketserver" standard library module to write a server.

from socketserver import BaseRequestHandler, TCPServer, ThreadingMixIn
import zen_utils


class ZenHandler(BaseRequestHandler):
    def handle(self):
        zen_utils.handler_conversation(self.request, self.client_address)


class ZenServer(ThreadingMixIn, TCPServer):
    allow_reuse_address = 1


if __name__ == '__main__':
    address = zen_utils.parse_command_line("legacy server")
    server = ZenServer(address, ZenHandler)
    server.serve_forever()
