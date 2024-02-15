from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pageObjects import registrationPage


class AccountPage:
    def __init__(self, driver):
        self.driver = driver

    account_dashboard_labels = (By.XPATH, "//tbody/tr/td[1]")
    account_dashboard_values = (By.XPATH, "//tbody/tr/td[2]")
    address_book_button = (By.LINK_TEXT, "地址簿")
    address_book_addresses = (By.ID, "sylius-default-address")
    orders_summary_button = (By.LINK_TEXT, "我的订单")
    order_summary_dates = (By.XPATH, "//tbody/tr/td[3]")
    order_summary_totals = (By.XPATH, "//tbody/tr/td[6]")
    order_summary_numbers = (By.XPATH, "//tbody/tr/td[1]")

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
