import json
import logging

import requests

from config import settings


class HeadframeApi:
    url_base: str = 'https://pool.headframe.io/api'
    url: str = f'{url_base}/backend/v0.1'
    token: str
    cookie: dict

    def __init__(self, token: str):
        self.token = token
        self.cookie = {
            'ory_session_relaxedwescoffeywmz1r7og': self.token,
        }

    """
    BASE
    """

    def request_get(self, url: str):
        r = requests.get(url=url, cookies=self.cookie)
        json_data = r.json()
        logging.critical(f'GET {url} | {json.dumps(json_data)}')
        return json_data

    def request_post(self, url: str, data: dict = None):
        r = requests.post(url=url, data=data, cookies=self.cookie)
        json_data = r.json()
        logging.critical(f'POST {url} | {json.dumps(json_data)}')
        return json_data

    def request_delete(self, url: str, data: dict = None):
        r = requests.delete(url=url, data=data, cookies=self.cookie)
        json_data = r.json()
        logging.critical(f'DELETE {url} | {json.dumps(json_data)}')
        return json_data

    """
    API
    """

    def create_boundary(self, name: str, recipient_miner_id: str, donor_miner_id: str, hash_rate: int) -> dict:
        url = f'{self.url}/workers/boundary'
        return self.request_post(
            url=url,
            data={
                "name": name,
                "recipient_miner_id": recipient_miner_id,
                "donor_miner_id": donor_miner_id,
                "hashrate": hash_rate,
            },
        )

    def delete_boundary(self, worker_id: str) -> dict:
        url = f'{self.url}/workers/boundary/{worker_id}'
        return self.request_post(url=url)

    """
    API PLUS
    """

    def get_miner_workers(self, miner_id: str) -> list[dict]:
        url = f'{self.url}/miners/{miner_id}/workers'
        result = self.request_get(url=url)
        return [
            {
                'id': worker['id'],
                'name': worker['name'],
                'type': worker['behavior'],
                'status': worker['status'],
            }
            for worker in result.get('data', [])
        ]


headframe_api = HeadframeApi(token=settings.token)
