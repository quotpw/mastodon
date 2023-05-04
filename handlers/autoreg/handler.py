import random
import time
import uuid
from io import BytesIO

from handlers.autoreg.types import Args, Statistic
from handlers.helpers import randomize_text, append_to_file
from helpers.mastodon import Mastodon
from . import constants

stats = Statistic()


def thread_handler(thread_id: str, args: Args):
    while True:
        mail = None
        try:
            proxy = args.proxies.iter_get()
            print(thread_id, f"Starting registration with {proxy}")

            client = Mastodon(proxy)

            print(thread_id, "Getting oauth token")
            client.oauth_token()

            mail = args.kopeechka.get_mail(
                "mastodon.social",
                ["ALL"],
                regex='(confirmation_token=.*?)("|&)'
            )

            username = mail.mail.split("@")[0] + str(random.randint(1000, 99999))
            print(thread_id, "Creating account with mail", mail.mail, "and username", "@" + username)
            client.create_account(mail.mail, username, mail.mail + "!")

            print(thread_id, "Wait for confirmation mail")
            confirmation_token = mail.wait_for_message(120)
            if not confirmation_token:
                raise Exception("Confirmation mail not found")

            confirmation_token = confirmation_token[19:-1]
            print(thread_id, "Confirmation token:", confirmation_token)

            client.verify_mail(confirmation_token)
            print(thread_id, "Mail verified")

            files = {
                "display_name": (None, randomize_text(args.display_name)),
                "fields_attributes[]": (None, ""),
            }
            if len(args.avatars) > 0:
                files["avatar"] = (
                    f"{uuid.uuid4()}.png",
                    BytesIO(random.choice(args.avatars)),
                    "image/png"
                )
            if len(args.headers) > 0:
                files["header"] = (
                    f"{uuid.uuid4()}.png",
                    BytesIO(random.choice(args.headers)),
                    "image/png"
                )

            print(thread_id, "Updating profile")
            client.patch(
                '/api/v1/accounts/update_credentials',
                files=files
            )

            print(thread_id, "Account registered")
            args.stats.registered += 1
            append_to_file(
                constants.save_path,
                'tokens.txt',
                ':'.join([
                    username,
                    mail.mail,
                    mail.mail + "!",
                    client.access_token
                ])
            )
        except Exception as err:
            print(f"{thread_id} {err}")
            args.stats.errors += 1
            time.sleep(1)
            continue

        if mail is not None:
            mail.cancel()
