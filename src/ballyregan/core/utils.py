import asyncio
import requests

def has_internet_connection() -> bool:
    """Check wether or not the system is connected to a network

    Returns:
        bool: Connected or not
    """
    try:
        requests.get('https://www.google.com')
    except:
        return False
    else:
        return True


def get_event_loop():
    try:
        return asyncio.get_running_loop() 
    except Exception:
        return asyncio.get_event_loop_policy().get_event_loop()
