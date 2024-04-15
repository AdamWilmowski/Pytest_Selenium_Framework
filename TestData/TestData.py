from faker import Faker
import random


class RandomData:

    def __init__(self):
        self.fake = Faker('zh_CN')

    def generate_random_chinese_info(self):
        company = self.fake.company()
        vat_number = random.randint(100000000000000, 999999999999999)
        address_full = self.fake.address()
        address_split = address_full.split()
        registered_address = address_split[0]
        office_phone = random.randint(1000000000000, 9999999999999)
        bank = self.fake.bank()
        bank_number = random.randint(100000000000000000000000000000, 999999999999999999999999999999)
        detailed_address = self.fake.street_address()
        phone_number = random.randint(1000000000000, 9999999999999)
        name = self.fake.first_name()
        surname = self.fake.last_name()
        customer_data = {
            'company': company,
            'vat_number': vat_number,
            'registered_address': registered_address,
            'office_phone': office_phone,
            'bank_name': bank,
            'bank_number': bank_number,
            'detailed_address': detailed_address,
            'phone_number': phone_number,
            'name': name,
            'surname': surname,
        }
        return customer_data


random_data = RandomData()
data = random_data.generate_random_chinese_info()
print(data)


class ProductData:
    one_product = "AX-178"

