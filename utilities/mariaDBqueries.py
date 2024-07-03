class MariaDBSQLQueries:
    @staticmethod
    def basic_products_query():
        return """SELECT
            sp.code,
            sp.moq,
            sp.duty,
            sp.multiple,
            spv.weight,
            bt.qty,
            bt.price
        FROM
            sylius_product sp
        JOIN sylius_product_variant spv ON
            sp.code = spv.code
        JOIN sylius_plus_inventory_source_stock spiss ON
            spv.id = spiss.product_variant_id
        JOIN brille24_tierprice bt ON
            spv.id = bt.product_variant_id
            AND sp.enabled = 1
            AND sp.show_pip = 1 
            AND sp.allowed_for_DS90 = 1
            AND spiss.on_hand > 0
            AND bt.customer_group_id = 1
        LIMIT 50
        """

    @staticmethod
    def heavy_products_query():
        return """
        SELECT
            sp.code,
            sp.moq,
            sp.duty,
            sp.multiple,
            spv.weight,
            bt.qty,
            bt.price
        FROM
            sylius_product sp
        JOIN sylius_product_variant spv ON
            sp.code = spv.code
        JOIN sylius_plus_inventory_source_stock spiss ON
            spv.id = spiss.product_variant_id
        JOIN brille24_tierprice bt ON
            spv.id = bt.product_variant_id
            AND sp.enabled = 1
            AND sp.show_pip = 1 
            AND sp.allowed_for_DS90 = 1
            AND spiss.on_hand > 10
            AND bt.customer_group_id = 1
            AND spv.weight > 10000
        LIMIT 50
        """

    @staticmethod
    def expensive_products_query():
        return """
        SELECT
            sp.code,
            sp.moq,
            sp.multiple,
            spv.weight,
            bt.qty,
            bt.price
        FROM
            sylius_product sp
        JOIN sylius_product_variant spv ON
            sp.code = spv.code
        JOIN sylius_plus_inventory_source_stock spiss ON
            spv.id = spiss.product_variant_id
        JOIN brille24_tierprice bt ON
            spv.id = bt.product_variant_id
            AND sp.enabled = 1
            AND sp.show_pip = 1 
            AND sp.allowed_for_DS90 = 1
            AND spiss.on_hand > 0
            AND bt.customer_group_id = 1
            AND bt.price > 1000000000
        LIMIT 50
        """
