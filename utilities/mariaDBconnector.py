import json

import mariadb
import sys
from TestData.Secrets import Secrets

try:
    conn = mariadb.connect(
        host="172.25.130.21",
        port=3306,
        user=Secrets.maria_db_user,
        password=Secrets.maria_db_password,
        database="betacn32")
except mariadb.Error as e:
    print(f"Error connecting to the database: {e}")
    sys.exit(1)
print("Connection established")
conn.close()


class MariaDBConnector:
    def __init__(self, db_version):
        self.sql = mariadb.connect(
                    host="172.25.130.21",
                    port=3306,
                    user=Secrets.maria_db_user,
                    password=Secrets.maria_db_password,
                    database=db_version)
        self.cursor = self.sql.cursor(dictionary=True)

    def get_basic_products(self):
        sql_query = """
        SELECT sp.code, sp.moq, sp.multiple, spv.weight, bt.qty, bt.price
        FROM sylius_product sp
        JOIN sylius_product_variant spv ON sp.code = spv.code
        JOIN sylius_plus_inventory_source_stock spiss ON spv.id = spiss.product_variant_id
        JOIN brille24_tierprice bt ON spv.id = bt.product_variant_id
        AND sp.enabled = 1
        AND sp.show_pip = 1
        AND sp.allowed_for_DS90 = 1
        AND spiss.on_hand > 0
        AND bt.customer_group_id = 1
        LIMIT 50
        """
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        with open("products_data_raw.json", "w") as f:
            json.dump(result, f, indent=4)

