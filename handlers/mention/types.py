from dataclasses import dataclass

from helpers.proxy import ProxyCounter
from helpers.string import StringCounter


class Statistic:
    posted: int = 0
    errors: int = 0


@dataclass
class Args:
    work: bool
    stats: Statistic

    proxies: ProxyCounter
    tokens: StringCounter
    users: StringCounter
    text: str
