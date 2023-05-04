import time

from handlers.trends_parser.types import Args, Statistic
from handlers.helpers import append_to_file
from helpers.mastodon import Mastodon
from . import constants

stats = Statistic()


def thread_handler(args: Args):
    offset = 0
    client = Mastodon(args.proxies.iter_get())
    all_users = set()
    while True:
        try:
            users = set()
            trend_statuses = client.get_trend_statuses(offset, 40)
            if len(trend_statuses) < 1:
                print("No more users")
                return
            offset += len(trend_statuses)
            for status in trend_statuses:
                user = ':'.join([status['account']['acct'], status['account']['id']])
                if user not in all_users:
                    all_users.add(user)
                    users.add(user)
            args.stats.parsed += len(users)
            print(f"Parsed: {args.stats.parsed}; Fetched: {len(users)}")
            append_to_file(constants.save_path, 'users.txt', '\n'.join(users))
        except Exception as err:
            print(err)
            time.sleep(10)
