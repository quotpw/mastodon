import datetime
import time

import requests

from ..api import APIClass
from . import constants
from . import helpers


class Mastodon(APIClass):
    def __init__(self, proxy: str = None, account: str = None):
        self.session = requests.Session()
        self.session.verify = False
        self.session.proxies = {"http": proxy, "https": proxy} if proxy else None
        self.access_token = None
        self.rate_limit = {
            'limit': 300,
            'remaining': 300,
            'reset': time.time() + 900
        }
        super().__init__(
            self,
            constants.BASE_URL,
            {
                "User-Agent": "Mastodon/310 CFNetwork/1335.0.3.1 Darwin/21.6.0",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
            }
        )

        if account is not None:
            self.account = account.split(':')
            self.account = {
                'username': self.account[0],
                'mail': self.account[1],
                'password': self.account[2],
                'token_type': 'Bearer',
                'access_token': self.account[3]
            }
            self.set_auth(self.account)
        else:
            self.account = None

        self.pre_middlewares.append(self.pre_middleware)
        self.post_middlewares.append(self.post_middleware)

    def id(self):
        if self.account is not None:
            return f"[{self.account['username']}]"
        else:
            return "[Mastodon]"

    def pre_middleware(self, method: str, url: str, kwargs: dict):
        if self.rate_limit['remaining'] <= 1:
            print(self.id(), "Rate limit exceeded, waiting for reset")
            time.sleep(self.rate_limit['reset'] - time.time())
        return method, url, kwargs

    def post_middleware(self, method: str, url: str, kwargs: dict, response: requests.Response):
        h = response.headers
        if h.get('x-ratelimit-limit'):
            self.rate_limit['limit'] = int(h['x-ratelimit-limit'])
        if h.get('x-ratelimit-remaining'):
            self.rate_limit['remaining'] = int(h['x-ratelimit-remaining'])
        if h.get('x-ratelimit-reset'):
            self.rate_limit['reset'] = int(datetime.datetime.fromisoformat(h['x-ratelimit-reset'][:-1]).timestamp())

    def set_auth(self, data: dict):
        self.access_token = data["access_token"]
        self.headers["Authorization"] = f"{data['token_type']} {data['access_token']}"

    def oauth_token(self):
        response = self.post(
            "/oauth/token",
            json={
                "client_id": constants.CLIENT_ID,
                "scope": "read write follow push",
                "redirect_uri": "mastodon://joinmastodon.org/oauth",
                "client_secret": constants.CLIENT_SECRET,
                "grant_type": "client_credentials"
            }
        ).json()
        self.set_auth(response)
        return response

    def create_account(self, email, username, password):
        response = self.post(
            "/api/v1/accounts",
            json={
                "email": email,
                "username": username,
                "password": password,
                "reason": "",
                "agreement": True,
                "locale": "en"
            }
        ).json()
        self.set_auth(response)
        return response

    def verify_mail(self, confirmation_token: str):
        return self.get(
            '/auth/confirmation',
            params={
                "confirmation_token": confirmation_token,
                "redirect_to_app": "true"
            },
            allow_redirects=False
        )

    def get_trend_statuses(self, offset=0, limit=100):
        return self.get(
            '/api/v1/trends/statuses',
            params={
                'offset': str(offset),
                'limit': str(limit)
            }
        ).json()

    def get_community_statuses(self, max_id=None, limit=100):
        params = {
            'local': 'true',
            'limit': str(limit)
        }
        if max_id:
            params['max_id'] = max_id

        response = self.get(
            '/api/v1/timelines/public',
            params=params
        )

        return response.json(), helpers.extract_link(response)

    def get_subscribers(self, user_id: str, max_id: int = None):
        params = {'limit': '80'}
        if max_id:
            params['max_id'] = str(max_id)
        response = self.get(
            f'/api/v1/accounts/{user_id}/followers',
            params=params
        )
        return response.json(), helpers.extract_link(response)

    def private_mention(self, text: str):
        return self.post(
            '/api/v1/statuses',
            files={
                'status': (None, text),
                'sensitive': (None, 'false'),
                'visibility': (None, 'direct'),
                'language': (None, 'en')
            }
        ).json()
