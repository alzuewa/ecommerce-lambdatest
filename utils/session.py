from typing import Optional

import requests
from requests import Session

from utils.logger import logger


class ApiSession(Session):

    def __init__(self, base_url, cookies: Optional[dict | list[dict]] = None):
        super().__init__()
        self.base_url = base_url
        if cookies:
            self.cookies = cookies

    @logger
    def request(self, endpoint_path: str, method: str, **kwargs) -> requests.Response:
        url = f'{self.base_url}{endpoint_path}'
        if self.cookies:
            return super().request(url=url, method=method, cookies=self.cookies, **kwargs)
        else:
            return super().request(url=url, method=method, **kwargs)

    def get(self, endpoint_path: str, **kwargs) -> requests.Response:
        return self.request(endpoint_path, method='GET', **kwargs)

    def post(self, endpoint_path: str, **kwargs) -> requests.Response:
        return self.request(endpoint_path, method='POST', **kwargs)

    def put(self, endpoint_path: str, **kwargs) -> requests.Response:
        return self.request(endpoint_path, method='PUT', **kwargs)

    def patch(self, endpoint_path: str, **kwargs) -> requests.Response:
        return self.request(endpoint_path, method='PATCH', **kwargs)

    def delete(self, endpoint_path: str, **kwargs) -> requests.Response:
        return self.request(endpoint_path, method='DELETE', **kwargs)
