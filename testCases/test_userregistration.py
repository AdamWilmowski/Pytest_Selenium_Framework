from pageObjects.mainPage import MainPage
from utilities.BaseClass import BaseClass
from TestData.TestData import RandomData
from TestData.SQLConnection import SQLFunctions
from pageObjects.loginPage import LoginPage
from pageObjects.accountPage import AccountPage


class TestUserRegistration(BaseClass):

    def test_register_user_basic(self):
        main_page = MainPage(self.driver)
        db_version = main_page.get_db_version()
        sql_function = SQLFunctions()
        registration_page = main_page.get_to_registration_page()
        random_data = RandomData()
        customer_data = random_data.generate_random_chinese_info()
        email_value = sql_function.get_email_value()
        customer_email = "chinacustomertme" + email_value + "@gmail.com"
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
        registration_page.select_all_agreements()
        registration_page.get_register_button().click()
        sql_function.add_customer_to_database(
            email_value, customer_data["company"], customer_data["vat_number"], customer_data["registered_address"],
            customer_data["office_phone"], customer_data["bank_name"], customer_data["bank_number"],
            customer_data["detailed_address"], customer_data["phone_number"], customer_data["name"],
            customer_data["surname"], customer_data["phone_number"], customer_email, db_version
        )
        sql_function.close_connection()
        list_to_compare = [
            customer_data["company"], customer_data["vat_number"], customer_data["registered_address"],
            customer_data["office_phone"], customer_email, customer_email, customer_data["phone_number"],
            customer_data["name"], customer_data["surname"]
        ]
        welcome_page_items = registration_page.get_welcome_page_items_list()
        for i in range(len(list_to_compare)):
            assert list_to_compare[i] == welcome_page_items[i]

        #FUNCTION FOR CHECKING THE DATABASE ACTIVATION LINK

        link_from_function = "" #retrieved link
        self.get_to(link_from_function)
        registration_page.input_first_password()
        registration_page.input_second_password()
        registration_page.get_save_password_button().click()
        login_page = LoginPage(self.driver)
        login_page.input_username(customer_email)
        login_page.input_password("1qaz@WSX")
        login_page.get_login_button().click()
        assert customer_data["company"] in main_page.get_page_header().text
        main_page.get_page_header().click()
        account_page = main_page.get_to_account_dashboard()
        account_values_company = account_page.get_account_dashboard_values_dict("company")
        for data in account_values_company:
            assert account_values_company[data] == customer_data[data]
        address_book_dict = account_page.get_address_from_address_book(0)
        for address in address_book_dict:
            assert address_book_dict[address] == customer_data[address]

