import time
from ballyregan import ProxyFetcher

start = time.time()
proxy_fetcher = ProxyFetcher(background_gather=True, debug=False)
for _ in range(3):
    try:
        proxies = proxy_fetcher.get(limit=1)
    except:
        pass
        time.sleep(1)
    else:
        print(proxies)
        print(f"Operation took {time.time() - start} seconds")
    