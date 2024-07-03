import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
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
    form_order = (By.CSS_SELECTOR, 'form[class="ui loadable form"]')
    grand_total = (By.XPATH, "//tr/td[8]")
    submit_order = (By.ID, "create-button")
    transport_cost_button = (By.ID, "js-split-transport-costs")
    transport_cost_input = (By.ID, "split-transport-costs-total-value")
    transport_cost_save_button = (By.XPATH, '//div[10]/div/div[3]/button')
    order_label = (By.CSS_SELECTOR, "i[class='inbox icon']")

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

    def wait_for_form_to_reload(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(AdminPage.form_order)
        )

    def get_grand_total(self):
        elements = self.driver.find_elements(*AdminPage.grand_total)
        grand_total_raw = elements[-1].text
        grand_total = grand_total_raw.split()[1]
        return float(grand_total)

    def add_transport_costs(self, transport_costs):
        self.driver.find_element(*AdminPage.transport_cost_button).click()
        self.driver.find_element(*AdminPage.transport_cost_input).send_keys(transport_costs)
        time.sleep(0.5)
        self.driver.find_element(*AdminPage.transport_cost_save_button).click()
        time.sleep(0.5)
        self.wait_for_form_to_reload()

    def get_to_submit_order(self):
        self.driver.find_element(*AdminPage.submit_order).click()

    def wait_for_text_in_order_label(self, text):
        WebDriverWait(self.driver, 60*6).until(
            EC.text_to_be_present_in_element(AdminPage.order_label, text)
        )
