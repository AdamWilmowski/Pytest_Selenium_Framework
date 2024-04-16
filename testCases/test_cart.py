import pytest
import json
from utilities.BaseClass import BaseClass
from pageObjects.mainPage import MainPage


class TestCart(BaseClass):
    @pytest.mark.parametrize("get_product_data", ["basic_products"], indirect=True)
    def test_add_to_cart(self, get_product_data):
        main_page = MainPage(self.driver)
        main_page.close_cookies()
        with open("../JSON_files/products_data.json") as products:
            products = json.load(products)
        product_list = list(products.keys())[:2]
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
        prices_list_product_1 = sorted(list((products[product_list[0]]["prices"]).values()))
        moq_product_1 = products[product_list[0]]["moq"]
        multiply_product_1 = products[product_list[0]]["multiply"]
        thresholds_product_1 = products[product_list[0]["threshold"]]
        list_of_products_total = cart_page.get_list_of_product_attributes("price_total")
        assert list_of_products_total[0] == moq_product_1 * prices_list_product_1[0]
        cart_page.input_product_qty(0, thresholds_product_1[0])
        list_of_products_total = cart_page.get_list_of_product_attributes("price_total")
        assert list_of_products_total[0] == prices_list_product_1[1] * thresholds_product_1[1]
        cart_page.increase_product_qty(0)
        list_of_products_total = cart_page.get_list_of_product_attributes("price_total")
        total_product_1 = prices_list_product_1[1] * thresholds_product_1[0] + multiply_product_1
        assert list_of_products_total[0] == total_product_1
        prices_list_product_2 = sorted(list((products[product_list[1]]["prices"]).values()))
        moq_product_2 = products[product_list[1]]["moq"]
        multiply_product_2 = products[product_list[1]]["multiply"]
        thresholds_product_2 = products[product_list[1]["threshold"]]
        total_product_2 = prices_list_product_2[0] * moq_product_2
        total_order = total_product_1 + total_product_2
        assert total_order == cart_page.get_order_total()