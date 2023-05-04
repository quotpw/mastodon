import time
from handlers.community_parser.types import Args, Statistic
from handlers.helpers import append_to_file
from helpers.mastodon import Mastodon
from . import constants

stats = Statistic()


def thread_handler(args: Args):
    client = Mastodon(args.proxies.iter_get())
    max_id = None
    all_users = set()
    community_statuses = None
    while True:
        try:
            users = set()
            community_statuses, link_params = client.get_community_statuses(max_id, 40)
            if link_params.get('next') is None:
                print("No more users")
                return
            max_id = link_params['next']['max_id']

            for status in community_statuses:
                user = ':'.join([status['account']['acct'], status['account']['id']])
                if user not in all_users:
                    all_users.add(user)
                    users.add(user)

            args.stats.parsed += len(users)
            print(f"Parsed: {args.stats.parsed}; Fetched: {len(users)}")
            if len(community_statuses) < 1:
                print("No more users")
                return
            append_to_file(constants.save_path, 'users.txt', '\n'.join(users))
        except Exception as err:
            print(community_statuses, err)
            time.sleep(10)
