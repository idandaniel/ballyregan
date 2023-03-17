<h1>🔷 Ballyregan</h1>
<p><em>Find fetch & validate free proxies fast.</em></p>

<p>
  <a href="https://pypi.org/project/ballyregan" target="_blank">
      <img src="https://img.shields.io/pypi/v/ballyregan?label=pypi%20package" alt="Package version">
  </a>
  <a href="https://pypi.org/project/ballyregan" target="_blank">
      <img src="https://img.shields.io/pypi/pyversions/ballyregan.svg?color=%2334D058" alt="Supported Python versions">
  </a>
  <a href="https://pypi.org/project/ballyregan" target="_blank">
      <img src="https://img.shields.io/badge/license-Apache%202.0-yellow" alt="License: Apache 2.0">
  </a>
</p>

---

<br>

Ballyregan is a package & CLI that allows you to fetch free tested proxies really fast!

Key features:
  * **Fetch** free tested proxies super fast with [ProxyFetcher](https://github.com/idandaniel/ballyregan/blob/main/src/ballyregan/fetcher.py)
  * **Validate** your own proxies with [ProxyValidator](https://github.com/idandaniel/ballyregan/blob/main/src/ballyregan/validator.py)
  * **Filter** custom proxy list by protocol & anonymity with [ProxyFilterer](https://github.com/idandaniel/ballyregan/blob/main/src/ballyregan/filterer.py)

<br>

---

## How does it work?
When you use the ProxyFetcher to fetch a proxy, it performs several steps:
1. Gather all the available proxies from a list of built in providers (each provider gathers it's own and returns it to the fetcher).

  - > Provider - any website that serves free proxy lists (e.g https://free-proxy-list.net).

2. Filter all the gathered proxies by the given protocols and anonymities (if exist).
3. Validate the filtered proxies and return them.

<br>

> **Note** <br>
> You can write and append your own custom providers and pass it to the ProxyFetcher class as attribute. <br>
> Every custom proxy provider must implement the [IProxyProvider](https://github.com/idandaniel/ballyregan/blob/main/src/ballyregan/providers/interface.py) base interface.

<br>

## Behind the scenes
Fetching a proxy is an [IO bound operation](https://en.wikipedia.org/wiki/I/O_bound) which depends on network. A common approach for this problem is performing your network requests async. <br>
After digging a bit, testing Threads, Greenlets and async operations, we decided to go the async way. <br>
To perform async http requests, ballyregan uses [aiohttp](https://docs.aiohttp.org/en/stable/) and [asyncio](https://docs.python.org/3/library/asyncio.html),
as <em>"asyncio is often a perfect fit for IO-bound and high-level structured network code."</em> (from asyncio docs). <br>
By using the power of async http requests, ballyregan is able to validate thousands of proxies really fast. <br>

---

## Install

```sh
pip install ballyregan
```

## Usage

### 📦 Package

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

### 💻 CLI

#### Get all proxies
```sh
ballyregan get --all
```

#### Get one proxy
```sh
ballyregan get
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
ballyregan get -l 4
```

#### Get proxies by filters
```sh
ballyregan get -l 4 -p https -p socks5 -a elite
```

---

## 👤 Author

**Idan Daniel**

* Github: [@idandaniel](https://github.com/idandaniel)

## 📝 License

Copyright © 2022 [Idan Daniel](https://github.com/idandaniel).<br />
This project is [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) licensed.

