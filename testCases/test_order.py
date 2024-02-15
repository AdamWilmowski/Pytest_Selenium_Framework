import datetime
from pageObjects.mainPage import MainPage
from utilities.BaseClass import BaseClass


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

