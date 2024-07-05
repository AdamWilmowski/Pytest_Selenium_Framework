import time
from random import randint

import pytest
import json
import random
from utilities.BaseClass import BaseClass
from pageObjects.mainPage import MainPage
from utilities.fixtures import get_product_data


class TestCart(BaseClass):
    @pytest.mark.parametrize("get_product_data", ["basic_products"], indirect=True)
    def test_add_to_cart(self, get_product_data):
        number_of_products = 2
        main_page = MainPage(self.driver)
        main_page.close_cookies()
        with open("../JSON_files/products_data.json") as products:
            products = json.load(products)

        product_list = random.sample(list(products.keys()), number_of_products)
        number_of_products_in_cart = 0
        for product in product_list:
            main_page.search_for_product(product)
            main_page.add_product_to_cart_listing(0)
            number_of_products_in_cart += 1
            main_page.wait_till_product_in_cart(str(number_of_products_in_cart))
            self.get_to_main()
        cart_page = main_page.get_to_cart()

        list_of_codes = cart_page.get_list_of_product_attributes("code")
        for i in range(len(list_of_codes)):
            assert list_of_codes[i] == product_list[i]

        for i, product_id in enumerate(product_list):
            product = products[product_id]
            product_threshold = [str(x) for x in product["threshold"]]
            product_prices = product["prices"]
            product_moq = product["moq"]
            product_multiply = product["multiple"]
            product_total = product["moq"] * product_prices[product_threshold[0]]
            product_weight = product["weight"]

            setattr(self, f'product_{i}_threshold', product_threshold)
            setattr(self, f'product_{i}_prices', product_prices)
            setattr(self, f'product_{i}_total', product_total)
            setattr(self, f'product_{i}_moq', product_moq)
            setattr(self, f'product_{i}_multiply', product_multiply)
            setattr(self, f'product_{i}_weight', product_weight)

        products_total = cart_page.get_list_of_product_attributes("price_total")

        current_total = 0
        current_weight = 0
        for i in range(len(product_list)):
            assert products_total[i] == round(getattr(self, f'product_{i}_total'), 4)
            current_total += getattr(self, f'product_{i}_total')
            current_weight += getattr(self, f'product_{i}_weight') * getattr(self, f'product_{i}_moq')
        if current_weight > 1000:
            current_weight = round(current_weight / 1000, 5)
        order_total = cart_page.get_order_total()
        weight_total = cart_page.get_weight_total()
        assert order_total == round(current_total, 4)
        assert weight_total == round(current_weight, 4)
        cart_page.increase_product_qty(0)
        product_price_1 = self.product_0_prices[self.product_0_threshold[0]]
        product_price_2 = self.product_0_prices[self.product_0_threshold[1]]
        if self.product_0_moq + self.product_0_multiply < int(self.product_0_threshold[1]) \
                or len(self.product_0_threshold) < 2:
            price_increase = self.product_0_multiply * product_price_1
        else:
            price_increase = self.product_0_multiply * product_price_2
        time.sleep(5)
        products_total = cart_page.get_list_of_product_attributes("price_total")
        order_total = cart_page.get_order_total()
        assert products_total[0] == self.product_0_total + price_increase
        assert order_total == round(current_total + price_increase, 4)
        cart_page.input_product_qty(1, self.product_1_threshold[-1])
        time.sleep(4)
        products_total = cart_page.get_list_of_product_attributes("price_total")
        assert products_total[1] == \
               float(self.product_1_threshold[-1]) * self.product_1_prices[self.product_1_threshold[-1]]