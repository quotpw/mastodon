from typing import List, Callable

import requests


class APIClass:
    def __init__(self, root, base_url: str, default_headers: dict = None):
        self.root = root
        self.base_url = base_url
        self.headers = self.root.session.headers if default_headers is None else default_headers

        self.pre_middlewares: List[Callable] = []
        # func(method: str, url: str, kwargs: dict) -> (method:str, url:str, kwargs:dict)

        self.middlewares: List[Callable] = []
        # func(method: str, url: str, kwargs: dict, response: requests.Response) -> (retry:bool, method:str, url:str, kwargs:dict)

        self.post_middlewares: List[Callable] = []
        # func(method: str, url: str, kwargs: dict, response: requests.Response) -> None

        self.retry = 0
        self.timeout = 10

    def handle_pre_middleware(self, method: str, url: str, kwargs: dict) -> (str, str, dict):
        for pre_middleware in self.pre_middlewares:
            method, url, kwargs = pre_middleware(method, url, kwargs)
        return method, url, kwargs

    def handle_middleware(self, method: str, url: str, kwargs: dict, response: requests.Response) -> (bool, str, str, dict):
        for middleware in self.middlewares:
            retry, method, url, kwargs = middleware(method, url, kwargs, response)
            if retry:
                return retry, method, url, kwargs
        return False, method, url, kwargs

    def handle_post_middleware(self, method: str, url: str, kwargs: dict, response: requests.Response):
        for post_middleware in self.post_middlewares:
            post_middleware(method, url, kwargs, response)

    def prepare_headers(self, headers: dict = None):
        if headers is None:
            headers = {}
        headers.update(self.headers)
        return headers

    def prepare_request(self, method: str, path: str, kwargs: dict):
        method = method.lower()

        url = path
        if not path.startswith("http"):
            if not path.startswith("/"):
                path = "/" + path
            url = self.base_url + path

        kwargs["headers"] = self.prepare_headers(kwargs.get("headers"))

        return self.handle_pre_middleware(method, url, kwargs)

    def handle_request(self, method: str, path: str, **kwargs):
        method, url, kwargs = self.prepare_request(method, path, kwargs)  # Pre middleware: maybe need request modification

        try_number = 0

        error = None
        while try_number <= self.retry:
            try:
                response = self.root.session.request(method, url, **kwargs)

                # Middleware: check for retry needed
                retry, method, url, kwargs = self.handle_middleware(method, url, kwargs, response)
                if retry:
                    continue

                for post_middleware in self.post_middlewares:
                    post_middleware(method, url, kwargs, response)

                return response
            except requests.exceptions.RequestException as err:
                error = err
                try_number += 1

        raise error

    def post(self, path: str, params: dict = None, data: dict = None, json: dict = None, headers: dict = None, **kwargs) -> requests.Response:
        return self.handle_request(
            "post",
            path,
            params=params,
            data=data,
            json=json,
            headers=headers,
            **kwargs
        )

    def patch(self, path: str, params: dict = None, data: dict = None, json: dict = None, headers: dict = None, **kwargs) -> requests.Response:
        return self.handle_request(
            "patch",
            path,
            params=params,
            data=data,
            json=json,
            headers=headers,
            **kwargs
        )

    def get(self, path: str, params: dict = None, headers: dict = None, **kwargs) -> requests.Response:
        return self.handle_request(
            "get",
            path,
            params=params,
            headers=headers,
            **kwargs
        )
