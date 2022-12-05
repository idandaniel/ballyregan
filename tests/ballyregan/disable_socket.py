import socket
from functools import wraps


def disable_socket(func):
    original_socket = socket.socket

    @wraps(func)
    def socket_disabled_before(*args, **kwargs):
        def guard(*args, **kwargs):
            raise Exception('Attempted to access network')

        socket.socket = guard
        return func(*args, **kwargs)

    socket.socket = original_socket
    
    return socket_disabled_before
