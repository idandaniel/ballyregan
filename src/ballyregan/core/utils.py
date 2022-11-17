import os
import platform

from typing import List

from ballyregan import Proxy


def split_list_to_chunks(lst: list, chunks_count: int) -> List[list]:
    """Gets a list and return the list splitted to [chunks_amount] chunks

    Args:
        lst (list): The list to split
        chunks_count (int): The amount of chunk the list will be splitteed into.

    Returns:
        List[list]: List of [chunks_amount] lists.
    """
    return [lst[i::chunks_count] for i in range(chunks_count)]


def make_requests_proxies_dict_from_proxy(proxy: Proxy) -> dict:
    """takes a proxy model and returns a dict that requests package is able to use as 'proxies' is request

    Args:
        proxy (Proxy): Proxy model

    Returns:
        dict: the requests proxies dict
    """
    if 'socks' in proxy.protocol:
        return {
            'http': str(proxy),
            'https': str(proxy)
        }
    return {proxy.protocol: str(proxy)}


def has_internet_connection() -> bool:
    """Check wether or not the system is connected to a network

    Returns:
        bool: Connected or not
    """
    os_type = platform.system()
    null_device = "NUL" if os_type.lower() == "windows" else "/dev/null"
    return os.system(f"ping 8.8.8.8 -n 2 -w 2 > {null_device}") == 0
