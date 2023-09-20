import asyncio

import socket


def has_internet_connection() -> bool:
    try:
        s = socket.create_connection(("8.8.8.8", 53), timeout=2)
        s.close()
        return True
    except:
        return False


def get_event_loop():
    try:
        return asyncio.get_running_loop() 
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop
