import threading
import time

from handlers.subscribers_parser.handler import thread_handler
from handlers.subscribers_parser.types import Args, Statistic
from handlers.helpers import *
from helpers.proxy import ProxyCounter
from helpers.string import StringCounter


def statistics(args: Args):
    while args.work:
        set_console_title(f"Parsed: {args.stats.parsed}; Users: {args.users.available()}")
        time.sleep(1)


def start():
    proxies = ProxyCounter(default_input("Path to proxies", "proxies.txt"))
    users = StringCounter(default_input("Path to users", "users.txt"))

    thread_count = default_input("Thread count", 10)
    if thread_count > proxies.count():
        thread_count = proxies.count()
    if thread_count > users.count():
        thread_count = users.count()

    args = Args(
        work=True,
        stats=Statistic(),
        users=users,
        proxies=proxies,
    )

    threading.Thread(target=statistics, args=(args,)).start()

    threads = []
    print("Starting", thread_count, "threads")
    for i in range(thread_count):
        t = threading.Thread(target=thread_handler, args=(f"[{i}]", args,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    args.work = False
