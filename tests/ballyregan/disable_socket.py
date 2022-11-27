import socket



def run_offline(func):
    original_socket = socket.socket

    def socket_disabled_before(*args, **kwargs):

        def guard(*args, **kwargs):
            raise Exception('Attempted to access network')

        socket.socket = guard
        return func(*args, **kwargs)

    socket.socket = original_socket
    return socket_disabled_before
