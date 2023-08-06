import os
from json.decoder import JSONDecodeError
from typing import Any, Dict
from urllib.parse import urljoin

import requests
from requests.exceptions import HTTPError

from vidispine.collections import Collection
from vidispine.errors import APIError, ConfigError, NotFound
from vidispine.items import Item, ItemShape
from vidispine.jobs import Job
from vidispine.log import Log
from vidispine.metadata import MetadataField, MetadataFieldGroup
from vidispine.search import Search
from vidispine.typing import BaseJson, ClientResponse

PROTOCOL = 'https'


class Client:

    def __init__(
        self,
        url: str = None,
        user: str = None,
        password: str = None,
    ) -> None:

        url = self._check_config('VIDISPINE_URL', 'url', url)
        user = self._check_config('VIDISPINE_USER', 'user', user)
        pwd = self._check_config('VIDISPINE_PASSWORD', 'password', password)

        if not url.startswith('http'):
            url = f'{PROTOCOL}://{url}'

        self.base_url = urljoin(url, '/API/')
        self.auth = (user, pwd)

    def _check_config(
        self,
        env_var: str,
        name: str,
        attribute: str = None,
    ) -> str:

        if attribute:
            return attribute

        try:
            return os.environ[env_var]
        except KeyError:
            error = f'Missing {name} or {env_var} not set'
            raise ConfigError(error)

    def _generate_headers(self) -> Dict[str, str]:
        return {
            'content-type': 'application/json',
            'accept': 'application/json'
        }

    def _request(
        self,
        method: str,
        url: str,
        headers: dict = None,
        json: dict = None,
        data: Any = None,
        params: dict = None,
        runas: str = None,
    ) -> ClientResponse:

        url = urljoin(self.base_url, url)
        request_kwargs: Any = {
            'method': method,
            'url': url,
            'auth': self.auth,
            'params': params,
        }

        tmp_headers = self._generate_headers()
        if headers:
            tmp_headers.update({k.lower(): v for k, v in headers.items()})

        if runas:
            tmp_headers.setdefault('runas', runas)

        # Vidispine throws an error if content-type supplied with no payload
        if method.upper() == 'GET' or (not json and not data):
            tmp_headers.pop('content-type')

        request_kwargs['headers'] = tmp_headers

        if json:
            request_kwargs['json'] = json
        if data:
            request_kwargs['data'] = data

        response = requests.request(**request_kwargs)

        try:
            response.raise_for_status()
        except HTTPError as err:
            if response.status_code == 404:
                raise NotFound(
                    f'Not Found: {method} - {url} - {response.text}'
                )
            else:
                raise APIError(
                    f'Vidispine Error: {method} - {url} - {response.text}'
                ) from err

        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> ClientResponse:
        """Pass-through request method

        This is to be used for functionality that has not yet been
        implemented.
        """
        kwargs['url'] = url.lstrip('/')
        kwargs['method'] = method
        return self._request(**kwargs)

    def get(self, url: str, **kwargs: Any) -> Any:
        kwargs['url'] = url
        kwargs['method'] = 'GET'
        return self._request(**kwargs)

    def post(self, url: str, **kwargs: Any) -> Any:
        kwargs['url'] = url
        kwargs['method'] = 'POST'
        return self._request(**kwargs)

    def put(self, url: str, **kwargs: Any) -> Any:
        kwargs['url'] = url
        kwargs['method'] = 'PUT'
        return self._request(**kwargs)

    def delete(self, url: str, **kwargs: Any) -> Any:
        kwargs['url'] = url
        kwargs['method'] = 'DELETE'
        return self._request(**kwargs)


class Vidispine:

    def __init__(
        self,
        url: str = None,
        user: str = None,
        password: str = None,
    ) -> None:

        self.client = Client(url, user, password)
        self.collection = Collection(self.client)
        self.item = Item(self.client)
        self.item_shape = ItemShape(self.client)
        self.job = Job(self.client)
        self.log = Log(self.client)
        self.metadata_field = MetadataField(self.client)
        self.metadata_field_group = MetadataFieldGroup(self.client)
        self.search = Search(self.client)

    def version(self) -> BaseJson:
        return self.client.get('version')

    def reindex(self, index: str, params: dict = None) -> BaseJson:
        if params is None:
            params = {}

        endpoint = f'reindex/{index}'

        return self.client.put(endpoint, params=params)
