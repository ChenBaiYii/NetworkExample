#!/usr/bin/python3
# asynchronous I/O inside 'asyncio' callback methods.

import asyncio
import zen_utils


class ZenServer(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.data = b''
        print('accepted connection from {}.'.format(self.address))

    def data_received(self, data):
        self.data += data
        if self.data.endswith(b'?'):
            answer = zen_utils.get_answer(self.data)
            self.transport.write(answer)
            self.data = b''

    def connection_lost(self, exc):
        if exc:
            print("client {} error: {}".format(self.address, exc))
        elif self.data:
            print("client {} sent {} but then closed".format(self.address, self.data))
        else:
            print("client {} closed socket".format(self.address))


if __name__ == '__main__':
    address = zen_utils.parse_command_line("asyncio server using callbacks")
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ZenServer, *address)
    server = loop.run_until_complete(coro)
    print("listening at {}".format(address))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()
