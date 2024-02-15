from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver

    grand_total = (By.ID, "sylius-summary-grand-total")
    checkout_next_step = (By.ID, "next-step")
    place_order = (By.ID, "place-order")
    payment_gate_title = (By.TAG_NAME, 'h1')
    payment_gate_amount = (By.TAG_NAME, 'h3')
    payment_gate_yes_button = (By.CSS_SELECTOR, 'input[class="ui button green"]')
    thank_you_values = (By.CSS_SELECTOR, 'span[class="font-weight-light"]')


    def get_checkout_grand_total(self):
        total_raw = self.driver.find_element(*CheckoutPage.grand_total).text
        total = float(total_raw.split()[1])
        return total

    def get_to_next_step(self):
        self.driver.find_element(*CheckoutPage.grand_total).click()

    def get_to_place_order(self):
        self.driver.find_element(*CheckoutPage.place_order).click()

    def wait_for_payment_gate(self):
        WebDriverWait(self.driver, 60*6).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'h1'))
        )

    def get_payment_gate_title(self):
        return self.driver.find_element(*CheckoutPage.payment_gate_title).text

    def get_payment_gate_amount(self):
        return float(self.driver.find_element(*CheckoutPage.payment_gate_amount).text.split()[1])

    def accept_payment(self):
        self.driver.find_element(*CheckoutPage.payment_gate_yes_button).click()

    def get_thank_you_values(self):
        elements_list_raw = self.driver.find_elements(*CheckoutPage.thank_you_values)
        elements_dict = {
            "order_number": elements_list_raw[0].text,
            "total": elements_list_raw[1].text.split()[1],
            "payment_type": elements_list_raw[4].text
        }
        return elements_dict


