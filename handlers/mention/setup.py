import threading
import time

from handlers.mention.handler import thread_handler
from handlers.mention.types import Args, Statistic
from handlers.helpers import *
from helpers.proxy import ProxyCounter
from helpers.string import StringCounter


def statistics(args: Args):
    while args.work:
        set_console_title(f"Posted: {args.stats.posted}; Errors: {args.stats.errors}; Users: {args.users.available()}; Tokens: {args.tokens.available()}")
        time.sleep(1)


def start():
    proxies = ProxyCounter(default_input("Path to proxies", "proxies.txt"))
    tokens = StringCounter(default_input("Path to tokens", "tokens.txt"))
    users = StringCounter(default_input("Path to users", "users.txt"))

    text = open(default_input("Path to text", "text.txt"), 'r', encoding='utf-8').read().strip()
    if not text:
        raise Exception("Text is empty")

    thread_count = default_input("Thread count", 10)
    if thread_count > proxies.count():
        thread_count = proxies.count()
    if thread_count > tokens.count():
        thread_count = tokens.count()
    if thread_count > users.count():
        thread_count = users.count()

    args = Args(
        work=True,
        stats=Statistic(),
        proxies=proxies,
        tokens=tokens,
        users=users,
        text=text
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
