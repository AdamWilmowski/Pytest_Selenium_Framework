from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class AccountPage:
    def __init__(self, driver):
        self.driver = driver

    account_dashboard_labels = (By.XPATH, "//tbody/tr/td[1]")
    account_dashboard_values = (By.XPATH, "//tbody/tr/td[2]")
    address_book_button = (By.LINK_TEXT, "地址簿")
    address_book_addresses = (By.ID, "sylius-default-address")

    # Order Section

    orders_summary_button = (By.LINK_TEXT, "我的订单")
    order_summary_dates = (By.XPATH, "//tbody/tr/td[3]")
    order_summary_totals = (By.XPATH, "//tbody/tr/td[6]")
    order_summary_numbers = (By.XPATH, "//tbody/tr/td[1]")

    # Company User Section

    company_user_section = (By.LINK_TEXT, "用户")
    add_company_user_button = (By.CSS_SELECTOR, 'a[class="button -primary d-inline-block m-t-20"]')
    select_role = (By.CSS_SELECTOR, 'div[class="ui dropdown selection"]')
    default_user_role = (By.CSS_SELECTOR, 'div[class="item"]')
    company_user_name = (By.ID, "app_new_company_user_customer_firstName")
    company_user_surname = (By.ID, "app_new_company_user_customer_lastName")
    company_user_email = (By.ID, "app_new_company_user_customer_email")
    company_user_phone_number = (By.ID, "app_new_company_user_customer_phoneNumber")
    company_user_validation = (By.CSS_SELECTOR, 'div[class="ui red pointing label sylius-validation-error"]')
    add_button = (By.CSS_SELECTOR, 'button[class="button -primary"]')
    company_user_list_emails = (By.XPATH, "//tbody/tr/td[2]")
    company_user_list_roles = (By.XPATH, "//tbody/tr/td[3]")
    company_user_list_statuses = (By.XPATH, "//tbody/tr/td[4]")

    # Reset Password Section

    reset_password_section = (By.LINK_TEXT, "更改密码")
    reset_password_current_password = (By.ID, "sylius_user_change_password_currentPassword")
    reset_password_new_password = (By.ID, "sylius_user_change_password_newPassword_first")
    reset_password_new_password_confirm = (By.ID, "sylius_user_change_password_newPassword_second")
    reset_password_button = (By.CSS_SELECTOR, 'button[class="button -primary -fullWidth"]')

    def get_account_dashboard_values_dict(self, choice=None):
        values_list = self._fetch_values()
        labels_list = self._fetch_labels()
        if choice == "company":
            company_dict = {
                "company": values_list[1],
                "vat_number": values_list[2],
                "registered_address": values_list[3],
                "office_phone": values_list[4],
                "bank_name": values_list[5],
                "bank_number": values_list[6]
            }
            return company_dict
        elif choice == "ship_to":
            ship_to_details_dict = {
                "company": values_list[7],
                "country": values_list[8],
                "province": values_list[9],
                "city": values_list[10],
                "district": values_list[11],
                "detailed_address": values_list[12],
                "phone_number": values_list[13],
                "zip_code": values_list[14]
            }
            return ship_to_details_dict
        elif choice == "contact_person":
            contact_person_dict = {
                "surname": values_list[15],
                "name": values_list[16],
                "phone_number": values_list[17],
                "email": values_list[18]
            }
            return contact_person_dict
        elif choice == "values":
            return values_list
        elif choice == "labels":
            return labels_list
        else:
            raise ValueError(f"Invalid choice: {choice}. Expected, 'company', 'ship_to', 'contact_person', "
                             f"'values', or 'labels'.")

    def _fetch_values(self):
        values = self.driver.find_elements(*AccountPage.account_dashboard_values)
        return [value.text for value in values]

    def _fetch_labels(self):
        labels = self.driver.find_elements(*AccountPage.account_dashboard_labels)
        return [label.text for label in labels]

    def get_to_address_book(self):
        self.driver.find_element(*AccountPage.address_book_button).click()

    def get_address_from_address_book(self, index: int) -> dict:
        address = self.driver.find_elements(*AccountPage.address_book_addresses)[index].text
        address_list_full = address.split()
        if index == 0:
            address_list = address_list_full[3:]
            address_dict = {
                "company": address_list[0],
                "vat_number": address_list[1],
                "registered_address": address_list[2],
                "bank_name": address_list[3],
                "bank_number": address_list[4],
                "office_phone": address_list[6]
            }
            return address_dict
        else:
            address_list = address_list_full
            address_dict = {
                "company": address_list[0],
                "sap_id": address_list[1],
                "province": address_list[2].replace(",", ""),
                "city": address_list[3].replace(",", ""),
                "district": address_list[4],
                "detailed_address": address_list[5],
                "zip_code": address_list[6],
                "country": address_list[7],
                "phone_number": address_list[8]
            }
            return address_dict

    def get_to_orders_summary(self):
        self.driver.find_element(*AccountPage.orders_summary_button).click()

    def get_order_dates(self):
        dates_list = [date.text for date in self.driver.find_elements(*AccountPage.order_summary_dates)]
        return dates_list

    def get_order_totals(self):
        total_list_raw = [total.text for total in self.driver.find_elements(*AccountPage.order_summary_totals)]
        total_list = [float(total.split()[1]) for total in total_list_raw]
        return total_list

    def get_order_numbers(self):
        order_numbers = [number.text for number in self.driver.find_elements(*AccountPage.order_summary_numbers)]
        return order_numbers

    def get_to_company_users(self):
        self.driver.find_element(*AccountPage.company_user_section).click()

    def add_new_company_user(self):
        self.driver.find_element(*AccountPage.add_company_user_button).click()

    def change_from_admin_to_default_user(self):
        self.driver.find_element(*AccountPage.select_role).click()
        self.driver.find_element(*AccountPage.default_user_role).click()

    def input_customer_name(self, text):
        self.driver.find_element(*AccountPage.company_user_name).send_keys(text)

    def input_customer_surname(self, text):
        self.driver.find_element(*AccountPage.company_user_surname).send_keys(text)

    def input_customer_emil(self, text):
        self.driver.find_element(*AccountPage.company_user_email).send_keys(text)

    def input_customer_phone(self, text):
        self.driver.find_element(*AccountPage.company_user_phone_number).send_keys(text)

    def clear_all_input_fields(self):
        self.driver.find_element(*AccountPage.company_user_name).clear()
        self.driver.find_element(*AccountPage.company_user_surname).clear()
        self.driver.find_element(*AccountPage.company_user_email).clear()
        self.driver.find_element(*AccountPage.company_user_phone_number).clear()

    def get_list_of_company_user_validations(self):
        elements = self.driver.find_elements(*AccountPage.company_user_validation)
        elements_text = [element.text for element in elements]
        return elements_text

    def add_company_user(self):
        self.driver.find_element(*AccountPage.add_button).click()

    def get_company_users_data_list(self, list_type):
        """
        Available list types:
        1. emails
        3. roles
        2. statuses
        """
        if list_type not in ["emails", "roles", "statuses"]:
            raise "Not Expected get_company_users_data_list function argument "
        list_attribute_name = f"company_user_list_{list_type}"
        list_of_elements = self.driver.find_elements(*getattr(AccountPage, list_attribute_name))
        list_of_elements_text = [i.text for i in list_of_elements]
        return list_of_elements_text

    def get_to_reset_password(self):
        self.driver.find_element(*AccountPage.reset_password_section).click()

    def input_reset_password_current_password(self, text):
        self.driver.find_element(*AccountPage.reset_password_current_password).send_keys(text)

    def input_reset_password_new_password(self, text):
        self.driver.find_element(*AccountPage.reset_password_new_password).send_keys(text)

    def input_reset_password_new_password_confirm(self, text):
        self.driver.find_element(*AccountPage.reset_password_new_password_confirm).send_keys(text)

    def reset_password(self):
        self.driver.find_element(*AccountPage.reset_password_button).click()
