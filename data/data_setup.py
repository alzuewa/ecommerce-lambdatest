from dataclasses import asdict

from . import models


def create_user():
    return models.User()


def create_user_request_data(user: models.User) -> dict:
    data = asdict(user)
    additional_data = {'customer_group_id': 1, 'confirm': data['password'], 'newsletter': 0, 'agree': 1}
    data.update(additional_data)
    return data


def create_product_request_data(product: models.Product):
    data = asdict(product)
    return data
