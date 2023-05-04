from dataclasses import dataclass

from helpers.proxy import ProxyCounter
from helpers.string import StringCounter


class Statistic:
    parsed: int = 0


@dataclass
class Args:
    work: bool
    stats: Statistic

    users: StringCounter
    proxies: ProxyCounter
