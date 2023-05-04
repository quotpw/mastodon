import time
from typing import List, Set

from handlers.subscribers_parser.types import Args, Statistic
from handlers.helpers import append_to_file
from helpers.mastodon import Mastodon
from . import constants

stats = Statistic()


def parse_users(thread_id: str, client: Mastodon, user: List[str]) -> Set[str]:
    users = set()
    max_id = None
    while True:
        followers, link_params = client.get_subscribers(user[1], max_id)
        if link_params.get('next') is None:
            break
        max_id = link_params['next']['max_id']

        added = 0
        for follower in followers:
            follower = ':'.join([follower['acct'], follower['id']])
            if follower not in users:
                added += 1
                users.add(follower)
        print(thread_id, f"Parsing: @{user[0]}", "Added:", added, "Total:", len(users))
    return users


def thread_handler(thread_id: str, args: Args):
    while args.users.available():
        try:
            user = args.users.get().split(':')
            if len(user) != 2:
                print(thread_id, "Invalid user")
                continue

            client = Mastodon(args.proxies.iter_get())

            users = parse_users(thread_id, client, user)

            print(thread_id, f"Finished parsing user: @{user[0]}. Users:", len(users))
            args.stats.parsed += len(users)

            append_to_file(constants.save_path, 'users.txt', '\n'.join(users))
        except Exception as err:
            print(err)
            time.sleep(10)
