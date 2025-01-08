import json
from decimal import Decimal

from requests import Response


def get_total_cart_price(response: Response) -> Decimal:
    string_with_price = json.loads(response.text)['total']
    price = string_with_price.split('$')[1].replace(',', '')
    return Decimal(price)


def get_price_repr(price) -> str:
    return f'{price:,}'
