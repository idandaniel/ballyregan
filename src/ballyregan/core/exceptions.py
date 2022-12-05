class ProxyException(Exception):
    """Base proxy exception
    """
    default_message: str = 'A generic proxy exception has occured'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(self.default_message, *args, **kwargs)


class ProxyGatherException(ProxyException):
    """Raised when a proxy gather fails
    """
    default_message: str = 'Failed to gather proxies.'


class ProxyParseException(ProxyException):
    """Raised when a proxy parse fails
    """
    default_message: str = 'Failed to parse raw proxy to Proxy model.'


class NoProxiesFound(ProxyException):
    """Raised when the requested amount of proxies is greater than the actual valid proxies the manager found.
    """
    default_message: str = 'Could not find any proxies'


class NoInternetConnection(Exception):
    pass


class InvalidDebugMode(Exception):
    pass
