import random
from . import constants


class ProxyCounter:
    def __init__(self, path):
        self.proxies = []
        self.index = 0
        with open(path, "r") as f:
            for line in f:
                proxy = line.strip().split(":")
                if len(proxy) == 2:
                    proxy_url = f"{proxy[0]}:{proxy[1]}"
                elif len(proxy) == 4:
                    proxy_url = f"{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}"
                else:
                    continue
                self.proxies.append(f"{constants.PROTO}://" + proxy_url)
        if len(self.proxies) == 0:
            raise Exception("No proxy found")
        random.shuffle(self.proxies)

    def iter_get(self):
        proxy = self.proxies[self.index]
        self.index += 1
        if self.index >= len(self.proxies):
            self.index = 0
        return proxy

    def count(self):
        return len(self.proxies)
