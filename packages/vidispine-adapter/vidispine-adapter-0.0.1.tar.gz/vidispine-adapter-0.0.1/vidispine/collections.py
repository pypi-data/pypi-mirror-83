from vidispine.errors import InvalidInput
from vidispine.typing import BaseJson


class Collection:

    def __init__(self, client) -> None:
        self.client = client

    def create(self, name: str) -> str:
        params = {'name': name}
        response = self.client.post('collection', params=params)

        return response['id']

    def get(self, vidispine_id: str, metadata: bool = True) -> BaseJson:
        endpoint = f'collection/{vidispine_id}'
        if metadata:
            endpoint = f'{endpoint}/metadata'

        return self.client.get(endpoint)

    def delete(self, vidispine_id: str) -> None:
        endpoint = f'collection/{vidispine_id}'

        self.client.delete(endpoint)

    def delete_multiple(self, vidispine_ids: list) -> None:
        if not vidispine_ids:
            raise InvalidInput('Please supply Vidispine IDs to delete.')

        params = {'id': ','.join(vidispine_ids)}
        endpoint = 'collection'

        self.client.delete(endpoint, params=params)

    def update_metadata(self, vidispine_id: str, metadata: dict) -> BaseJson:
        endpoint = f'collection/{vidispine_id}/metadata'

        return self.client.put(endpoint, json=metadata)

    def list(self, params: dict = None) -> BaseJson:
        endpoint = 'collection'

        return self.client.get(endpoint, params=params)
