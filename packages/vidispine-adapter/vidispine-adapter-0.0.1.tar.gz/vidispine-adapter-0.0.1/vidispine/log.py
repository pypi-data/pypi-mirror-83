from vidispine.typing import BaseJson


class Log:

    def __init__(self, client) -> None:
        self.client = client

    def list(self, params: dict = None) -> BaseJson:
        if params is None:
            params = {}

        endpoint = 'log'
        return self.client.get(endpoint, params=params)
