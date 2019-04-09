# single threaded server that serves one client at a time; others must wait.
# http://127.0.0.1:7478/pac/pdown.pac?t=1537344619798

import zen_utils

if __name__ == '__main__':
    address = zen_utils.parse_command_line("simple single threaded server")
    listener = zen_utils.create_srv_socket(address)
    zen_utils.accept_connections_forever(listener)
