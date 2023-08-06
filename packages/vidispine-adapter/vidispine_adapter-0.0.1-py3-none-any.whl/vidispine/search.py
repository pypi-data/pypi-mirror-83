from vidispine.typing import BaseJson
from vidispine.utils import create_matrix_params_query


class Search:

    def __init__(self, client) -> None:
        self.client = client

    def __call__(self, *args, **kwargs) -> BaseJson:
        return self._search(*args, **kwargs)

    def _search(
        self,
        metadata: dict = None,
        params: dict = None,
        matrix_params: dict = None
    ) -> BaseJson:

        return self._search_without_search_doc(params, matrix_params)

    def _search_without_search_doc(
        self,
        params: dict = None,
        matrix_params: dict = None
    ) -> BaseJson:

        if params is None:
            params = {}
        if matrix_params:
            endpoint = f'search/{create_matrix_params_query(matrix_params)}'
        else:
            endpoint = 'search'

        return self.client.get(endpoint, params=params)
