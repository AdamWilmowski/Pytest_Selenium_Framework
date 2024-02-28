import time
import pytest
from selenium.common import NoSuchElementException
from pageObjects.mainPage import MainPage
from utilities.BaseClass import BaseClass
from TestData.TestData import RandomData
from TestData.SQLConnection import SQLFunctions
from pageObjects.loginPage import LoginPage


class TestUserRegistration(BaseClass):

    def test_register_user_manual_helper(self):
        main_page = MainPage(self.driver)
        main_page.close_cookies()
        db_version = main_page.get_db_version()
        sql_function = SQLFunctions()
        registration_page = main_page.get_to_registration_page()
        random_data = RandomData()
        customer_data = random_data.generate_random_chinese_info()
        email_value = sql_function.get_email_value()
        customer_email = "chinacustomertme+" + str(email_value) + "@gmail.com"
        registration_page.get_zhu_fapiao()
        registration_page.input_company_name(customer_data["company"])
        registration_page.input_vat_number(customer_data["vat_number"])
        registration_page.input_registered_address(customer_data["registered_address"])
        registration_page.input_company_phone(customer_data["office_phone"])
        registration_page.input_bank_name(customer_data["bank_name"])
        registration_page.input_bank_number(customer_data["bank_number"])
        registration_page.input_send_to_company(customer_data["company"])
        registration_page.select_province()
        registration_page.input_send_to_detailed_address(customer_data["detailed_address"])
        registration_page.input_send_to_phone(customer_data["phone_number"])
        registration_page.input_contact_person_surname(customer_data["surname"])
        registration_page.input_contact_person_name(customer_data["name"])
        registration_page.input_contact_person_phone(customer_data["phone_number"])
        registration_page.input_contact_person_email(customer_email)
        registration_page.same_fapiao_email_switch()
        registration_page.select_all_agreements()
        time.sleep(20)

    @pytest.mark.registration
    def test_register_user_basic(self):
        main_page = MainPage(self.driver)
        main_page.close_cookies()
        db_version = main_page.get_db_version()
        sql_function = SQLFunctions()
        registration_page = main_page.get_to_registration_page()
        random_data = RandomData()
        customer_data = random_data.generate_random_chinese_info()
        email_value = sql_function.get_email_value()
        customer_email = "chinacustomertme+" + str(email_value) + "@gmail.com"
        registration_page.get_zhu_fapiao()
        registration_page.input_company_name(customer_data["company"])
        registration_page.input_vat_number(customer_data["vat_number"])
        registration_page.input_registered_address(customer_data["registered_address"])
        registration_page.input_company_phone(customer_data["office_phone"])
        registration_page.input_bank_name(customer_data["bank_name"])
        registration_page.input_bank_number(customer_data["bank_number"])
        registration_page.input_send_to_company(customer_data["company"])
        registration_page.select_province()
        registration_page.input_send_to_detailed_address(customer_data["detailed_address"])
        registration_page.input_send_to_phone(customer_data["phone_number"])
        registration_page.input_contact_person_surname(customer_data["surname"])
        registration_page.input_contact_person_name(customer_data["name"])
        registration_page.input_contact_person_phone(customer_data["phone_number"])
        registration_page.input_contact_person_email(customer_email)
        registration_page.same_fapiao_email_switch()
        registration_page.select_all_agreements()
        time.sleep(15)
        registration_page.register_customer()
        sql_function.add_customer_to_database(
            email_value, customer_data["company"], customer_data["vat_number"], customer_data["registered_address"],
            customer_data["office_phone"], customer_data["bank_name"], customer_data["bank_number"],
            customer_data["detailed_address"], customer_data["phone_number"], customer_data["name"],
            customer_data["surname"], customer_data["phone_number"], customer_email, db_version
        )
        list_to_compare = [
            customer_data["company"], str(customer_data["vat_number"]), customer_data["registered_address"],
            str(customer_data["office_phone"]), customer_email, customer_email, str(customer_data["phone_number"]),
            customer_data["name"], customer_data["surname"]
        ]
        welcome_page_items = registration_page.get_welcome_page_items_list()
        for i in range(len(list_to_compare)):
            assert list_to_compare[i] == welcome_page_items[i]
        time.sleep(10)
        set_password_link = self.get_hyperlinks_from_message()[7]
        self.get_to(set_password_link)
        registration_page.input_first_password()
        registration_page.input_second_password()
        registration_page.get_save_password_button().click()
        sql_function.confirmed_password(email_value)
        sql_function.close_connection()
        login_page = LoginPage(self.driver)
        login_page.input_username(customer_email)
        login_page.input_password("1qaz@WSX")
        login_page.get_login_button().click()
        assert customer_data["name"] in main_page.get_page_header().text
        current_url = self.get_current_url()
        if "account/agreements" in current_url:
            try:
                login_page.accept_after_login_agreement()
            except NoSuchElementException:
                pass
        main_page.get_page_header().click()
        account_page = main_page.get_to_account_dashboard()
        account_values_company = account_page.get_account_dashboard_values_dict("company")
        for data in account_values_company:
            assert account_values_company[data] == str(customer_data[data])
