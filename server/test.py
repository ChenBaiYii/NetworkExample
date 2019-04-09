#!/usr/bin/python3

import asyncio
import zen_utils


@asyncio.coroutine
def handle_conversation(reader, writer):
    print("r", reader)
    print("w", writer)
    print("over")
    address = writer.get_extra_info('peername')
    print("accepted connection from {}".format(address))
    while True:
        data = b''
        while not data.endswith(b"?"):
            more_data = yield from reader.read(4096)
            if not more_data:
                if data:
                    print("client {} sent {!r} but then closed".format(address, data))
                else:
                    print("client {} closed socket normally".format(address))
                return
            data += more_data
        answer = zen_utils.get_answer(data)
        writer.write(answer)


if __name__ == '__main__':
    address = zen_utils.parse_command_line("asyncio server using coroutine")
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_conversation, *address)
    server = loop.run_until_complete(coro)
    print("listening at {}".format(address))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()
