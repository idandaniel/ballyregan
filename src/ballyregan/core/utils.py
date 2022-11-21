from pythonping import ping

from ballyregan import Proxy


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
    try:
        ping('google.com', verbose=False, timeout=2, count=2)
    except:
        return False
    else:
        return True
