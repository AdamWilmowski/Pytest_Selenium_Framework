import time
import pytest
from selenium.common import NoSuchElementException
from pageObjects.mainPage import MainPage
from pageObjects.registrationPage import RegistrationPage
from utilities.BaseClass import BaseClass
from TestData.TestData import RandomData
from TestData.SQLConnection import SQLFunctions
from pageObjects.loginPage import LoginPage
from TestData.Secrets import Secrets


class TestCompanyUser(BaseClass):
    def test_add_company_user_admin(self):
        main_page = MainPage(self.driver)
        main_page.close_cookies()
        db_version = main_page.get_db_version()
        random_data = RandomData()
        customer_data = random_data.generate_random_chinese_info()
        sql_function = SQLFunctions()
        parent_email, parent_email_id = sql_function.get_random_customer_email_and_id(db_version)
        email_value = sql_function.get_email_value()
        email = "chinacustomertme+" + str(email_value) + "@gmail.com"
        login_page = main_page.get_to_login_page()
        login_page.input_username(parent_email)
        login_page.input_password(Secrets.default_password)
        login_page.get_login_button().click()
        self.get_to_main()
        main_page.get_page_header().click()
        account_page = main_page.get_to_account_dashboard()
        account_page.get_to_company_users()
        account_page.add_new_company_user()
        account_page.input_customer_name(customer_data['name'])
        account_page.input_customer_surname(customer_data['surname'])
        account_page.input_customer_emil(email)
        account_page.input_customer_phone(customer_data['phone_number'])
        account_page.add_company_user()
        company_user_email_list = account_page.get_company_users_data_list("emails")
        assert company_user_email_list[0] == email
        company_user_roles = account_page.get_company_users_data_list("roles")
        assert company_user_roles[0] == "公司管理员"
        company_user_statuses_list = account_page.get_company_users_data_list("statuses")
        assert company_user_statuses_list[0] == "未验证电子邮件"
        sql_function.add_company_user_to_database(1, customer_data['name'], customer_data['surname'],
                                                  customer_data['phone_number'], int(email_value), email,
                                                  int(parent_email_id), db_version)
        self.get_to_main()
        main_page.logout_customer()
        self.refresh()
        time.sleep(20)
        hyperlink = self.get_hyperlink_from_message()
        self.get_to(hyperlink)
        registration_page = RegistrationPage(self.driver)
        registration_page.input_first_password()
        registration_page.input_second_password()
        registration_page.get_save_password_button().click()
        sql_function.confirm_company_user(email_value)
        login_page.input_username(email)
        login_page.input_password(Secrets.default_password)
        login_page.get_login_button().click()
        current_url = self.get_current_url()
        if "account/agreements" in current_url:
            try:
                login_page.accept_after_login_agreement()
            except NoSuchElementException:
                pass
        assert customer_data["name"] in main_page.get_page_header().text






