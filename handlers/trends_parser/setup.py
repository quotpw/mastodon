import threading
import time

from handlers.trends_parser.handler import thread_handler
from handlers.trends_parser.types import Args, Statistic
from handlers.helpers import *
from helpers.proxy import ProxyCounter


def statistics(args: Args):
    while args.work:
        set_console_title(f"Parsed: {args.stats.parsed}")
        time.sleep(1)


def start():
    proxies = ProxyCounter(default_input("Path to proxies", "proxies.txt"))

    thread_count = 1  # default_input("Thread count", 10)
    if thread_count > proxies.count():
        thread_count = proxies.count()

    args = Args(
        work=True,
        stats=Statistic(),
        proxies=proxies,
    )

    threading.Thread(target=statistics, args=(args,)).start()

    threads = []
    print("Starting", thread_count, "threads")
    for i in range(thread_count):
        t = threading.Thread(target=thread_handler, args=(args,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    args.work = False
