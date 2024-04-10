import time
import json
from utilities.BaseClass import BaseClass
from utilities.fixtures import get_product_data
from pageObjects.mainPage import MainPage
from TestData.SQLConnection import SQLFunctions
from TestData.Secrets import Secrets
from pageObjects.accountPage import AccountPage


class TestCart(BaseClass):
    def test_add_to_cart(self, get_product_data):
        main_page = MainPage(self.driver)
        main_page.close_cookies()
        db_version = main_page.get_db_version()
        with open("../utilities/products_data.json") as products:
            products = json.load(products)
        product_list = list(products.keys())[::3]
        number_of_products_in_cart = 0
        for product in product_list:
            main_page.search_for_product(product)
            main_page.add_product_to_cart_listing(0)
            number_of_products_in_cart += 1
            main_page.wait_till_product_in_cart(str(number_of_products_in_cart))
            self.get_to_main()
