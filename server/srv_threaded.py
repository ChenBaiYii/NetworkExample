# using multiple threads to serve several clients in parallel

from threading import Thread
import zen_utils


def start_threads(listener, workers=4):
    t = (listener,)
    b = []
    for i in range(workers):
        print(f"{i}")
        # Thread(target=zen_utils.accept_connections_forever, args=t).start()
        s = Thread(target=zen_utils.accept_connections_forever, args=t)
        s.start()
        b.append(s)

    for i in b:
        i.join()

    print("直接结束")


if __name__ == '__main__':
    address = zen_utils.parse_command_line("multi-threaded server")
    listener = zen_utils.create_srv_socket(address)
    start_threads(listener)
