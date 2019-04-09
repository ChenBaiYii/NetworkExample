#!/usr/bin/python3
# asynchronous I/O driven directly by the poll() system call.

import select
import zen_utils


def all_events_forever(poll_object):
    """ 生成器反汇 fd event """
    while True:
        for fd, event in poll_object.poll():
            yield fd, event


def server(listener):
    sockets = {listener.fileno(): listener}  # listener.fileno() 返回一个文件描述符用于底层io操作 文件描述符: 套接字
    addresses = {}
    bytes_received = {}  # 接收缓冲区
    bytes_to_send = {}  # 发送缓冲区

    poll_object = select.poll()  # posix select 返回一个 fd_set 数据结构
    poll_object.register(listener, select.POLLIN)  # 注册监听套接字 默认为 poll input 模式
    for fd, event in all_events_forever(poll_object):
        sock = sockets[fd]
        # socket closed: remove it from our data structures.
        if event & (select.POLLHUP | select.POLLER | select.PLLNVAL):
            address = addresses.pop(sock)
            rb = bytes_received.pop(sock, b'')
            sb = bytes_to_send.pop(sock, b'')
            if rb:
                print("client {} send {} but then closed".format(address, rb))
            elif sb:
                print("client {} closed before we sent {}".format(address, sb))
            else:
                print("clint {} closed socket normally".format(address))
            poll_object.unregister(fd)
            del sockets[fd]
        # new socket: add it to our data structures.
        elif sock is listener:
            sock, address = sock.accept()
            print("accepted connection from {}".format(address))
            sock.setblocking(False)  # force socket.timeout if we blunder
            sockets[sock.fileno()] = sock  # 把套接字文件描述符和套接字本身做字典映射
            addresses[sock] = address  # 把套接字名在字典做映射
            poll_object.register(sock, select.POLLIN)  # 在 fd_set 数据结构中注册当前套接字并设定 poll in 状态
        # incoming data: keep receiving until we see the suffix
        elif event & select.POLLIN:
            more_data = sock.recv(4096)
            if not more_data:  # end of file
                sock.close()  # next poll() will POLLNVAL, and thus clean up
                continue
            data = bytes_received.pop(sock, b'') + more_data
            if data.endswith(b'?'):
                bytes_to_send[sock] = zen_utils.get_answer(data)
                poll_object.modify(sock, select.POLLOUT)
            else:
                bytes_received[sock] = data
        # socket ready to send: keep sending until all bytes are delivered.
        elif event & select.POLLOUT:
            data = bytes_to_send.pop(sock)
            n = sock.send(data)
            if n < len(data):
                bytes_to_send[sock] = data[n:]
            else:
                poll_object.modify(sock, select.POLLIN)


if __name__ == '__main__':
    address = zen_utils.parse_command_line("low-level async server")  # 返回一个 tuple 地址
    listener = zen_utils.create_srv_socket(address)  # 返回一个最大64个的监听套接字
    server(listener)
