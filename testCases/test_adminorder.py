import json
import time
import pytest
from utilities.BaseClass import BaseClass
from pageObjects.adminPage import AdminPage
from TestData.SQLConnection import SQLFunctions
from TestData.Secrets import Secrets
from utilities.fixtures import get_product_data


class TestAdminOrder(BaseClass):

    @pytest.mark.parametrize("test_data", [[2, "minimum"]])
    @pytest.mark.parametrize("get_product_data", ["basic_products"], indirect=True)
    def test_admin_order_basic(self, get_product_data, test_data):
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
        time.sleep(0.5)
        admin_page.wait_for_form_to_reload()
        order_total = 0
        for n in range(test_data[0]):
            admin_page.input_sku(products_list[n])
            product_n = products[products_list[n]]
            product_n_threshold = product_n["threshold"][0]
            admin_page.input_qty_and_add_to_order(product_n_threshold)
            order_total += product_n["prices"][str(product_n_threshold)] * product_n_threshold
            time.sleep(0.5)
            admin_page.wait_for_form_to_reload()
        grand_total = admin_page.get_grand_total()
        assert grand_total == round(order_total, 5)
        if order_total < 500:
            admin_page.add_transport_costs(0)
        admin_page.get_to_submit_order()
        admin_page.wait_for_text_in_order_label("Waiting for payment")

