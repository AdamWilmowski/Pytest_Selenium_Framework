import datetime
import time

import pytest
import json
import random
from pageObjects.mainPage import MainPage
from utilities.BaseClass import BaseClass
from TestData.TestData import RandomData
from TestData.SQLConnection import SQLFunctions
from TestData.TestData import ProductData
from utilities.fixtures import get_product_data


class TestOrders(BaseClass):

    @pytest.mark.parametrize("get_product_data", ["basic_products"], indirect=True)
    def test_order_basic(self, get_product_data):
        main_page = MainPage(self.driver)
        main_page.close_cookies()
        db_version = main_page.get_db_version()
        login_page = main_page.get_to_login_page()
        login_page.get_to_main_with_random_login(db_version)

        with open("../JSON_files/products_data.json", "r") as product_file:
            products = json.load(product_file)

        product_list = random.sample(products.keys(), 3)
        products_in_cart = 0
        order_total = 0
        for product in product_list:
            main_page.search_for_product(product)
            main_page.add_product_to_cart_listing(0)
            products_in_cart += 1
            product_prices = list(products[product]["prices"].values())
            product_moq = products[product]["moq"]
            order_total += product_prices[0] * product_moq
            main_page.wait_till_product_in_cart(str(products_in_cart))
            self.get_to_main()

        checkout_page = main_page.get_to_checkout()
        total = checkout_page.get_checkout_grand_total()
        if order_total < 500:
            order_total += 100
        assert total == round(order_total, 5)
        checkout_page.get_to_next_step()
        next_step_total = checkout_page.get_checkout_grand_total()
        assert next_step_total == round(order_total, 5)
        checkout_page.get_to_place_order()
        checkout_page.wait_for_payment_gate()
        checkout_page.select_payment_gate("b2b")
        payment_gate_amount = checkout_page.get_payment_gate_amount()
        assert payment_gate_amount == total
        checkout_page.accept_payment()
        thank_you_values = checkout_page.get_thank_you_values()
        assert thank_you_values["total"] == total
        assert thank_you_values["payment_type"] == "预付款"
        self.get_to_main()
        account_page = main_page.get_to_account_dashboard()
        account_page.get_to_orders_summary()
        assert account_page.get_order_dates()[0] == datetime.date.today().strftime("%m/%d/%Y")
        assert account_page.get_order_totals()[0] == round(order_total, 2)

