from dataclasses import dataclass
from helpers.proxy import ProxyCounter


class Statistic:
    parsed: int = 0


@dataclass
class Args:
    work: bool
    stats: Statistic

    proxies: ProxyCounter
