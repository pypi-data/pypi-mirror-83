from vidispine.errors import InvalidInput
from vidispine.typing import BaseJson


class Item:

    def __init__(self, client) -> None:
        self.client = client

    def get(
        self,
        item_id: str,
        params: dict = None,
        metadata=True
    ) -> BaseJson:

        if not params:
            params = {}

        if metadata:
            params.setdefault('content', 'metadata')

        endpoint = f'item/{item_id}'

        return self.client.get(endpoint, params=params)

    def delete(self, item_id: str) -> None:
        endpoint = f'item/{item_id}'
        self.client.delete(endpoint)

    def create_placeholder(
        self,
        metadata: dict,
        params: dict = None
    ) -> BaseJson:

        if params is None:
            params = {}

        params.setdefault('container', 1)
        endpoint = 'import/placeholder'

        return self.client.post(
            endpoint, json=metadata, params=params
        )

    def import_to_placeholder(
        self,
        item_id: str,
        component_type: str,
        params: dict
    ) -> None:

        if not params:
            raise InvalidInput('Please supply a URI or fileId.')

        endpoint = f'import/placeholder/{item_id}/{component_type}'

        return self.client.post(endpoint, params=params)


class ItemShape:

    def __init__(self, client) -> None:
        self.client = client

    def list(self, item_id: str, params: dict = None) -> BaseJson:
        if params is None:
            params = {}

        endpoint = f'item/{item_id}/shape'
        return self.client.get(endpoint, params=params)

    def import_shape(self, item_id: str, params: dict) -> None:
        if not params:
            raise InvalidInput('Please supply a URI or fileId.')

        endpoint = f'item/{item_id}/shape'

        return self.client.post(endpoint, params=params)
