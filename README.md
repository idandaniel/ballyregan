[![Python](https://img.shields.io/pypi/pyversions/ballyregan.svg)](https://badge.fury.io/py/ballyregan)
[![PyPI](https://badge.fury.io/py/ballyregan.svg?kill_cache=1)](https://badge.fury.io/py/ballyregan)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-yellow)](https://opensource.org/licenses/Apache-2.0)


# Ballyregan 🔷
## Find fetch & validate free proxies fast.

<br>

## How does it work?
Ballyregan fetches the proxies from  list of built in providers.
> Provider - any website that serves free proxy lists (e.g https://free-proxy-list.net).

You can write and append your own custom providers and pass it to the ProxyFetcher class as attribute. <br>
> **Note** <br>
> Every custom proxy provider must implement the [IProxyProvider](https://github.com/idandaniel/ballyregan/blob/main/src/ballyregan/providers/interface.py) base interface.

<br>

## Behind the scenes
Ballyregan uses [greenlets](https://greenlet.readthedocs.io/en/latest). <br>
Fetching a proxy is an [IO bound operation](https://en.wikipedia.org/wiki/I/O_bound) which depends on network, <br>
and greenlets provide concurrency, so by using them we are able validate thousands of proxies efficiently. <br>

<br>

## Install

```sh
pip install ballyregan
```

## Usage

### Package 📦

#### Create a fetcher instance
```python
from ballyregan import ProxyFetcher

# Setting the debug mode to True, defaults to False
fetcher = ProxyFetcher(debug=True)
```

#### Get one proxy
```python
proxy = fetcher.get_one()
print(proxy)
```

#### Get multiple proxies
```python
proxies = fetcher.get(limit=4)
print(proxies)
```

#### Get proxies by filters
```python
from ballyregan.models import Protocols, Anonymities

proxies = fetcher.get(
  limit=4,
  protocols=[Protocols.HTTPS, Protocols.SOCKS5],
  anonymities=[Anonymities.ELITE]
)
print(proxies)
```

### CLI 💻

#### Get all proxies
```sh
ballyregan get --all
```

#### Get one proxy
```sh
ballyregan get --all
```

#### Use debug mode
```sh
ballyregan --debug get [OPTIONS]
```

#### Format output to json
```sh
ballyregan get -o json
```

#### Get proxies by limit
```sh
bellyregan get -l 4
```

#### Get proxies by filters
```sh
bellyregan get -l 4 -p https -p socks5 -a elite
```

---

## Author

👤 **Idan Daniel**

* Github: [@idandaniel](https://github.com/idandaniel)

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2022 [Idan Daniel](https://github.com/idandaniel).<br />
This project is [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) licensed.

