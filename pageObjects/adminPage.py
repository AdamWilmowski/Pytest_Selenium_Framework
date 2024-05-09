from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AdminPage:
    def __init__(self, driver):
        self.driver = driver

    username = (By.ID, "_username")
    password = (By.ID, "_password")
    db_version = (By.XPATH, "//div[2]/div[5]/div/i")
    login_button = (By.CSS_SELECTOR, "button[class='ui fluid large primary submit button']")
    orders_button = (By.LINK_TEXT, "Orders")
    create_new_order_button = (By.LINK_TEXT, "Create New Order")
    customer_email_order = (By.ID, "sylius_admin_order_creation_new_order_customer_select_customerEmail")
    search_submit_button = (By.CSS_SELECTOR, "button[type='submit']")
    initial_place_order_button = (By.XPATH, "//td[8]/button")
    sku_input = (By.CSS_SELECTOR, "input[class='product-sku']")
    qty_input = (By.CSS_SELECTOR, "input[type='number']")
    cart_checkboxes = (By.CSS_SELECTOR, 'input[class="cart-item-checkbox"]')


    def input_username(self, text):
        self.driver.find_element(*AdminPage.username).send_keys(text)

    def input_password_and_login(self, text):
        self.driver.find_element(*AdminPage.password).send_keys(text)
        self.driver.find_element(*AdminPage.login_button).click()

    def getDBVersion(self):
        return self.driver.find_element(*AdminPage.db_version).text

    def get_to_orders(self):
        self.driver.find_element(*AdminPage.orders_button).click()

    def create_new_order(self):
        self.driver.find_element(*AdminPage.create_new_order_button).click()

    def input_customer_email_order(self, text):
        self.driver.find_element(*AdminPage.customer_email_order).send_keys(text)

    def submit_search_order(self):
        self.driver.find_element(*AdminPage.search_submit_button).click()

    def initial_place_order(self):
        self.driver.find_element(*AdminPage.initial_place_order_button).click()

    def input_sku(self, text):
        self.driver.find_element(*AdminPage.sku_input).send_keys(text)

    def input_qty_and_add_to_order(self, text):
        self.driver.find_element(*AdminPage.qty_input).send_keys(text)
        self.driver.find_element(*AdminPage.qty_input).send_keys(Keys.ENTER)

    def return_number_of_products(self):
        checkboxes = self.driver.find_elements(*AdminPage.cart_checkboxes)
        return len(checkboxes)





