from backend.config.dbconfig import dbconfig
import psycopg2


class CartContentsDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (dbconfig['database'],
                                                                            dbconfig['user'],
                                                                            dbconfig['password'],
                                                                            dbconfig['port'],
                                                                            dbconfig['host'])
        self.conn = psycopg2.connect(connection_url)

    def add_to_cart(self, cart_id, product_id, product_quantity):
        query = 'insert into "Cart_Contents"(cart_id, product_id, product_quantity) values(%s,%s,%s) returning cart_id, product_id, product_quantity;'
        cursor = self.conn.cursor()
        cursor.execute(query, (cart_id, product_id, product_quantity))
        result = cursor.fetchone()
        self.conn.commit()
        return result

    def remove_from_cart(self, cart_id, product_id):
        query = 'delete from "Cart_Contents" where cart_id = %s and product_id = %s;'
        cursor = self.conn.cursor()
        cursor.execute(query, (cart_id, product_id,))
        self.conn.commit()
        return cart_id, product_id

    def clear_cart(self, cart_id):
        query = 'delete from "Cart_Contents" where cart_id = %s returning cart_id;'
        cursor = self.conn.cursor()
        cursor.execute(query, (cart_id,))
        result = cursor.fetchone()[0]
        self.conn.commit()
        return result

    def in_cart(self, cart_id, product_id):
        query = 'select product_quantity from "Cart_Contents" where cart_id = %s and product_id = %s;'
        cursor = self.conn.cursor()
        cursor.execute(query, (cart_id, product_id))
        result = cursor.fetchone()
        return result

    def update_cart(self, cart_id, product_id, product_quantity):
        query = 'update "Cart_Contents" set cart_id = %s, product_id = %s, product_quantity = %s where cart_id = %s and product_id = %s;'
        cursor = self.conn.cursor()
        cursor.execute(query, (cart_id, product_id, product_quantity, cart_id, product_id))
        self.conn.commit()
        return cart_id, product_id, product_quantity


    def get_all_from_cart(self, cart_id):
        query = 'select cart_id, "Cart_Contents".product_id, "Cart_Contents".product_quantity, product_name, product_price * (1 - product_dis) ' \
                'from "Cart_Contents" inner join "Products" on "Products".product_id = "Cart_Contents".product_id where cart_id = %s and "Products".active = true;'
        cursor = self.conn.cursor()
        cursor.execute(query, (cart_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def delete_from_carts(self, product_id):
        query = 'delete from "Cart_Contents" where product_id = %s'
        cursor = self.conn.cursor()
        cursor.execute(query, (product_id,))
        self.conn.commit()
        return product_id

    def calculate_subtotal(self, cartId):
        query = 'select Sum("Products".product_price * "Cart_Contents".product_quantity * (1-product_dis)) as subtotal ' \
                'from "Cart_Contents" inner join "Products" on "Cart_Contents".product_id = "Products".product_id ' \
                'where cart_id=%s and "Products".active = true;'
        cursor = self.conn.cursor()
        cursor.execute(query, (cartId,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def delete_all_from_cart(self, cart_id, product_id):
        query = 'delete from "Cart_Contents" where cart_id=%s and product_id=%s'
        cursor = self.conn.cursor()
        cursor.execute(query, (cart_id, product_id,))
        self.conn.commit()
        return cart_id, product_id