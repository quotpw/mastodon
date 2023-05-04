import time
from typing import List

import requests

from ..api import APIClass


class Kopeechka(APIClass):
    def __init__(self):
        self.session = requests.Session()
        self.session.params = {
            "token": "2c0c001e90da1e3a4237a2c7789f3566",
            "type": "JSON",
            "api": "2.0"
        }
        super().__init__(self, "http://api.kopeechka.store")

    def get_balance(self):
        return self.get("/user-balance").json()['balance']

    def get_mail(self, domain: str, mail_type: List, sender: str = None, regex: str = None, clear: bool = True):
        params = {
            "site": domain,
            "mail_type": ",".join(mail_type),
            "clear": "1" if clear else "0"
        }
        if sender is not None:
            params["sender"] = sender
        if regex is not None:
            params["regex"] = regex

        return Email(self, self.get("/mailbox-get-email", params=params).json())


class Email:
    def __init__(self, main: Kopeechka, data: dict):
        if data.get('value') in ["BAD_SITE", "BAD_DOMAIN", "BAD_BALANCE", "OUT_OF_STOCK", "SYSTEM_ERROR", "TIME_LIMIT_EXCEED"]:
            raise Exception("Kopeechka error: " + data['value'])
        self.main = main
        self.id = data["id"]
        self.mail = data["mail"]

    def get_message(self, full: bool = False):
        response = self.main.get(
            "/mailbox-get-message",
            {
                "id": self.id,
                "full": "1" if full else "0"
            }
        ).json()

        if response["value"] == "WAIT_LINK":
            return None

        return response["fullmessage"] if full else response["value"]

    def cancel(self):
        self.main.get("/mailbox-cancel", {"id": self.id})

    def wait_for_message(self, wait_time: int = 3600, full: bool = False):
        until = time.time() + wait_time
        while time.time() < until:
            message = self.get_message(full)
            if message is not None:
                return message
            time.sleep(1)
        return None
