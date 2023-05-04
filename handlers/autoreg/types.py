from dataclasses import dataclass
from typing import List

from helpers.kopeechka import Kopeechka
from helpers.proxy import ProxyCounter


class Statistic:
    registered: int = 0
    errors: int = 0


@dataclass
class Args:
    work: bool
    stats: Statistic

    kopeechka: Kopeechka

    proxies: ProxyCounter
    display_name: str
    avatars: List[bytes]
    headers: List[bytes]
