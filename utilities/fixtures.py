import pytest
import json
from mariaDBconnector import MariaDBConnector

vat_number = 1.13
number_of_spaces = 0.00001


def transform_price_to_correct_float(integer):
    correct_value = integer * number_of_spaces * vat_number
    return round(correct_value, 5)


@pytest.fixture()
def get_product_data(request):
    query_type = request.param
    maria_db = MariaDBConnector("beta32")
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
                'prices': {}
            }
        transformed_data[code]['prices'][item['qty']] = item['price']
    for key, value in transformed_data.items():
        if isinstance(value, dict) and 'prices' in value:
            threshold_list = list(value['prices'].keys())
            value['threshold'] = threshold_list
            for price_key, price_value in value['prices'].items():
                value['prices'][price_key] = transform_price_to_correct_float(price_value)

    with open('../JSON_files/products_data.json', 'w') as file:
        json.dump(transformed_data, file, indent=4)

