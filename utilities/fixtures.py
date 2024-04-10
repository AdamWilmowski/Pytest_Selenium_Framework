import pytest
import json

vat_number = 1.13
number_of_spaces = 0.00001

@pytest.fixture()
def get_product_data(self):
    def transform_price_to_correct_float(integer):
        correct_value = integer * number_of_spaces * vat_number
        return round(correct_value, 5)

    with open('products_data_raw.json', 'r') as file:
        data = json.load(file)

    transformed_data = {}

    for item in data:
        code = item['code']
        if code not in transformed_data:
            transformed_data[code] = {
                'moq': item['moq'],
                'multiple': item['multiple'],
                'weight': item['weight'],
                'prices': {}
            }
        transformed_data[code]['prices'][item['qty']] = item['price']
    for key, value in transformed_data.items():
        if isinstance(value, dict) and 'prices' in value:
            for price_key, price_value in value['prices'].items():
                value['prices'][price_key] = transform_price_to_correct_float(price_value)

    with open('products_data.json', 'w') as file:
        json.dump(transformed_data, file, indent=4)

