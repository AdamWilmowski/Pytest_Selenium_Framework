from selenium.webdriver.common.by import By


class CartPage:
    def __init__(self, driver):
        self.driver = driver

    items_code = (By.CSS_SELECTOR, 'a[class="cart-item-panel-mpn text-size-medium"]')
    products_qty_input = (By.ID, "sylius_cart_item_quantity")
    arrow_up = (By.CSS_SELECTOR, 'i[class="caret right icon"]')
    arrow_down = (By.CSS_SELECTOR, 'i[class="caret left icon"]')
    items_weight = (By.CSS_SELECTOR, "span[data-update-field='weight']")
    items_unit_price = (By.CSS_SELECTOR, "span[data-update-field='unit-price']")
    items_price_total = (By.CSS_SELECTOR, "span[data-update-field='total']")
    total_weight = (By.CSS_SELECTOR, "span[data-update-field='weightTotal']")
    total = (By.CSS_SELECTOR, "span[data-update-field='orderTotal']")

    def get_list_of_product_attributes(self, list_type):
        if list_type not in ["code", "weight", "unit_price", "price_total"]:
            raise TypeError("Not Expected argument for get_list_of_product_attributes function")
        list_attribute_name = f"items_{list_type}"
        attributes = self.driver.find_elements(*getattr(CartPage, list_attribute_name))
        attributes_text = [x.text for x in attributes]
        if list_type == "code":
            return attributes_text
        if list_type == "weight":
            return [float(x.split()[0]) for x in attributes_text]
        if list_type == "unit_price" or list_type == "price_total":
            return [float(x.split()[1]) for x in attributes_text]

    def get_order_total(self):
        total_object = self.driver.find_elements(*CartPage.total)
        total = total_object.text.split()[1]
        return total

    def get_weight_total(self):
        weight_object = self.driver.find_elements(*CartPage.total_weight)
        weight = weight_object.text.split()[0]
        return weight
