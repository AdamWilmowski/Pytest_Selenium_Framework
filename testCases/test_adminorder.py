import json
import time
import pytest
from utilities.BaseClass import BaseClass
from pageObjects.adminPage import AdminPage
from TestData.SQLConnection import SQLFunctions
from TestData.Secrets import Secrets
from utilities.fixtures import get_product_data


class TestAdminOrder(BaseClass):

    @pytest.mark.parametrize("get_product_data", ["basic_products"], indirect=True)
    def test_admin_order_basic(self, get_product_data):
        self.stop_load()
        self.get_to_admin()
        admin_page = AdminPage(self.driver)
        admin_page.input_username(Secrets.admin_username)
        admin_page.input_password_and_login(Secrets.admin_password)

        with open("../JSON_files/products_data.json", "r") as product_file:
            products = json.load(product_file)

        products_list = list(products.keys())
        db_version = admin_page.getDBVersion()
        sql_function = SQLFunctions()
        customer_email = sql_function.get_random_customer(db_version)
        admin_page.get_to_orders()
        admin_page.create_new_order()
        admin_page.input_customer_email_order(customer_email)
        admin_page.submit_search_order()
        admin_page.initial_place_order()
        time.sleep(1)
        admin_page.input_sku(products_list[0])
        admin_page.input_qty_and_add_to_order(products[products_list[0]]["threshold"][0])
        time.sleep(2)
        admin_page.input_sku(products_list[1])
        admin_page.input_qty_and_add_to_order(products[products_list[1]]["threshold"][1])
        time.sleep(10)




