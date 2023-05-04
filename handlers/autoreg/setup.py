import threading
import time

from handlers.autoreg.handler import thread_handler
from handlers.autoreg.types import Args, Statistic
from handlers.helpers import *
from helpers.kopeechka import Kopeechka
from helpers.proxy import ProxyCounter


def statistics(args: Args):
    while args.work:
        set_console_title(f"Registered: {args.stats.registered}; Errors: {args.stats.errors}")
        time.sleep(1)


def start():
    proxies = ProxyCounter(default_input("Path to proxies", "proxies.txt"))
    display_name = open(default_input("Path to display name", "display_name.txt")).read().strip()
    avatars = get_png_files_as_bytes(default_input("Path to avatars", "avatars"))
    headers = get_png_files_as_bytes(default_input("Path to headers", "headers"))

    thread_count = default_input("Thread count", 10)
    if thread_count > proxies.count():
        thread_count = proxies.count()

    args = Args(
        work=True,
        stats=Statistic(),
        kopeechka=Kopeechka(),
        proxies=proxies,
        display_name=display_name,
        avatars=avatars,
        headers=headers
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
