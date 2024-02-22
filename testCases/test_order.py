import datetime
from pageObjects.mainPage import MainPage
from utilities.BaseClass import BaseClass
from TestData.TestData import RandomData
from TestData.SQLConnection import SQLFunctions


class TestOrders(BaseClass):
    def test_order_basic(self):
        main_page = MainPage(self.driver)
        main_page.close_cookies()
        db_version = main_page.get_db_version()
        login_page = main_page.get_to_login_page()
        login_page.get_to_main_with_random_login(db_version)
        main_page.search_for_product("USL1M-DIO")
        main_page.add_product_to_cart_listing(0)
        main_page.wait_till_product_in_cart(1)
        checkout_page = main_page.get_to_checkout()
        total = checkout_page.get_checkout_grand_total()
        assert total > 0
        checkout_page.get_to_next_step()
        next_step_total = checkout_page.get_checkout_grand_total()
        assert next_step_total == total
        checkout_page.get_to_place_order()
        checkout_page.wait_for_payment_gate()
        assert checkout_page.get_payment_gate_title() == "Payment gate symulation"
        assert checkout_page.get_payment_gate_amount() == total
        checkout_page.accept_payment()
        thank_you_values = checkout_page.get_thank_you_values()
        assert thank_you_values["total"] == total
        assert thank_you_values["payment_type"] == "预付款"
        self.get_to_main()
        account_page = main_page.get_to_account_dashboard()
        account_page.get_to_orders_summary()
        assert account_page.get_order_dates()[0] == datetime.date.today().strftime("%m/%d/%Y")
        assert account_page.get_order_totals()[0] == total

    def test_order_unregistered(self):
        main_page = MainPage(self.driver)
        main_page.close_cookies()
        db_version = main_page.get_db_version()
        sql_function = SQLFunctions()
        email_value = sql_function.get_email_value()
        email = "chinacustomertme+" + str(email_value) + "@gmail.com"
        random_data = RandomData()
        main_page.search_for_product("USL1M-DIO")
        main_page.add_product_to_cart_listing(0)
        main_page.wait_till_product_in_cart("1")
        checkout_page = main_page.get_to_checkout()
        customer = random_data.generate_random_chinese_info()
        checkout_page.select_zhu_fapiao()
        checkout_page.input_company_name(customer["company"])
        checkout_page.input_vat_number(customer["vat_number"])
        checkout_page.input_register_address_of_company(customer["registered_address"])
        checkout_page.input_office_number(customer["office_phone"])
        checkout_page.input_bank_name(customer["bank_name"])
        checkout_page.input_bank_number(customer["bank_number"])
        checkout_page.input_surname(customer["surname"])
        checkout_page.input_name(customer["name"])
        checkout_page.input_phone_number(customer["phone_number"])
        checkout_page.input_email(email)
        checkout_page.select_same_as_fapiao()
        checkout_page.get_to_next_step()
        checkout_page.select_province()
        checkout_page.input_company_name_shipping(customer["company"])
        checkout_page.input_detailed_address_shipping(customer["detailed_address"])
        checkout_page.input_phone_number_shipping(customer["phone_number"])
        checkout_page.get_to_next_step()
        checkout_page.select_all_agreements()
        checkout_page.get_to_place_order()
