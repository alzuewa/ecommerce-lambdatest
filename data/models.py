from dataclasses import dataclass
from uuid import uuid4

from dotenv import load_dotenv
from faker import Faker

load_dotenv()

fake = Faker('en_US')


@dataclass
class User:
    firstname: str
    lastname: str
    email: str
    telephone: str
    password: str

    def __init__(self):
        self.firstname = fake.first_name_male()
        self.lastname = fake.last_name_male()
        self.email = f'test-{uuid4()}@test.lambdatest'
        self.telephone = fake.phone_number()
        self.password = fake.password(length=12)


@dataclass
class Product:
    product_id: str
    quantity: str

    def __init__(self, product_id: str, quantity: str = '1'):
        self.product_id = product_id
        self.quantity = quantity
