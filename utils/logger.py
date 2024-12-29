import json
import logging
import sys
from collections.abc import Callable
from functools import wraps

import allure
from allure_commons.types import AttachmentType
from requests.exceptions import JSONDecodeError

from config import config

_logger = logging.getLogger(__name__)
console_formatter = logging.Formatter('\n==> {asctime} - [{levelname}] - {message}', style='{',
                                      datefmt='%Y-%m-%d %H:%M')
file_formatter = logging.Formatter('{asctime} - {levelname} - {message}', style='{', datefmt='%Y-%m-%d %H:%M')

console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setLevel('INFO')
console_handler.setFormatter(console_formatter)
_logger.addHandler(console_handler)

file_handler = logging.FileHandler('app.log', mode='w', encoding='utf-8')
file_handler.setLevel('DEBUG')
file_handler.setFormatter(file_formatter)
_logger.addHandler(file_handler)


def logger(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        initial_request_url = config.url + args[1]
        request_params = kwargs.get('params')
        if request_params:
            initial_request_url += f'?{request_params}'
        request_method = kwargs.get('method')
        request_data = kwargs.get('data')
        request_json = kwargs.get('json')
        request_headers = kwargs.get('headers')

        result = func(*args, **kwargs)
        try:
            allure.attach(
                body=json.dumps(result.json(), indent=4, ensure_ascii=True), name="Response",
                attachment_type=AttachmentType.JSON, extension="json"
            )
        except JSONDecodeError:
            allure.attach(
                body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt"
            )
        _logger.info(f'Request URL:: {initial_request_url}')
        _logger.info(f'Request method:: {request_method}')
        if result.request.body:
            _logger.info(f'Request body:: {result.request.body}')
        if request_data:
            _logger.info(f'Request body:: {request_data}')
        if request_json:
            _logger.info(f'Request body:: {request_json}')
        if request_headers:
            _logger.info(f'Request headers:: {request_headers}')
        _logger.info(f'Response status code:: {result.status_code}')
        _logger.info(f'Response text:: {result.text}\n')
        return result

    return wrapper
