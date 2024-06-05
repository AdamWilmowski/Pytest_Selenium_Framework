import pytest
import json
from utilities.mariaDBconnector import MariaDBConnector


@pytest.fixture()
def get_product_data(request):
    def transform_price_to_correct_float(integer: int, duty_rate: float):
        with open("../JSON_files/shop_data.json", "r") as shop_file:
            shop_data = json.load(shop_file)
        number_of_spaces = shop_data["number_of_spaces"]
        vat_rate = shop_data["vat_rate"]
        value_with_vat_rate = integer * number_of_spaces * vat_rate
        if duty_rate != 0.0:
            transformed_duty = duty_rate / 100 + 1
            value_with_vat_rate_and_duty = value_with_vat_rate * transformed_duty
            return round(value_with_vat_rate_and_duty, 5)
        else:
            return round(value_with_vat_rate, 5)

    query_type = request.param
    maria_db = MariaDBConnector("betacn33")
    if query_type == "basic_products":
        maria_db.get_basic_products()
    elif query_type == "heavy_products":
        maria_db.get_heavy_products()
    elif query_type == "expensive_products":
        maria_db.get_expensive_products()

    with open('../JSON_files/products_data_raw.json', 'r') as file:
        data = json.load(file)

    transformed_data = {}

    for item in data:
        code = item['code']
        if code not in transformed_data:
            transformed_data[code] = {
                'moq': item['moq'],
                'multiple': item['multiple'],
                'weight': item['weight'],
                'duty': item['duty'],
                'prices': {}
            }
        transformed_data[code]['prices'][item['qty']] = item['price']
    for key, value in transformed_data.items():
        if isinstance(value, dict) and 'prices' in value:
            threshold_list = list(value['prices'].keys())
            value['threshold'] = threshold_list
            for price_key, price_value in value['prices'].items():
                value['prices'][price_key] = transform_price_to_correct_float(price_value, value['duty'])

    with open('../JSON_files/products_data.json', 'w') as file:
        json.dump(transformed_data, file, indent=4)


