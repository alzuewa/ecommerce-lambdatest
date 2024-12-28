from pages.cart_page import CartPage
from pages.components.breadcrumb_bar import BreadcrumbBar
from pages.goods_page import GoodsPage
from pages.item_page import ItemPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.registration_page import RegistrationPage


class Application:
    def __init__(self):
        self.cart_page = CartPage()
        self.main_page = MainPage()
        self.login_page = LoginPage()
        self.breadcrumb_bar = BreadcrumbBar()
        self.goods_page = GoodsPage()
        self.item_page = ItemPage()
        self.registration_page = RegistrationPage()


app = Application()
