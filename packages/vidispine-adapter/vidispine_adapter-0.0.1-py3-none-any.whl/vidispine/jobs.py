from vidispine.typing import BaseJson


class Job:

    def __init__(self, client) -> None:
        self.client = client

    def get(self, job_id: str) -> BaseJson:
        endpoint = f'job/{job_id}'

        return self.client.get(endpoint)

    def list_problems(self) -> BaseJson:
        endpoint = 'job/problem'
        return self.client.get(endpoint)
