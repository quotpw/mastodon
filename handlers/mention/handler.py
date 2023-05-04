import time

from handlers.mention.types import Args, Statistic
from handlers.helpers import randomize_text
from helpers.mastodon import Mastodon
from . import constants

stats = Statistic()


def thread_handler(args: Args):
    while args.users.available() and args.tokens.available():
        client = Mastodon(args.proxies.iter_get(), args.tokens.get())
        try:
            for _ in range(constants.MAX_POSTS):
                if not args.users.available():
                    break

                text = randomize_text(args.text)
                while '<user>' in text and args.users.available():
                    user = args.users.get().split(':')
                    if len(user) != 2:
                        continue
                    text = text.replace('<user>', '@' + user[0], 1)

                mention = client.private_mention(text)
                print(client.id(), 'posted', mention['url'], 'with', len(text), 'chars')
                args.stats.posted += 1

                time.sleep(constants.SLEEP)
            print(client.id(), "posted", constants.MAX_POSTS, "posts")
        except Exception as err:
            args.stats.errors += 1
            print(client.id(), 'Error:', err)
