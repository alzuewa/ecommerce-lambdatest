import json
import locale
from decimal import Decimal

from requests import Response


def get_total_cart_price(response: Response) -> Decimal:
    string_with_price = json.loads(response.text)['total']
    price = string_with_price.split('$')[1].replace(',', '')
    return Decimal(price)


def get_price_repr(price) -> str:
    locale.setlocale(locale.LC_NUMERIC, 'en_US')
    return locale.format_string(f='%.2f', val=price, grouping=True)
