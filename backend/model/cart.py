from backend.config.dbconfig import dbconfig
import psycopg2

class CartDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (dbconfig['database'],
                                                                            dbconfig['user'],
                                                                            dbconfig['password'],
                                                                            dbconfig['port'],
                                                                            dbconfig['host'])
        self.conn = psycopg2.connect(connection_url)

    def create_cart(self, user_id):
        query = 'insert into "Cart"(user_id) values(%s) returning cart_id;'
        cursor = self.conn.cursor()
        cursor.execute(query, (user_id,))
        cart_id = cursor.fetchone()[0]
        self.conn.commit()
        return cart_id

    def get_all_carts(self):
        query ='select cart_id from "Cart";'
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_cart_by_id(self, cart_id):
        query = 'select cart_id from "Cart" where cart_id = %s;'
        cursor = self.conn.cursor()
        cursor.execute(query, (cart_id,))
        result = cursor.fetchone()
        return result

    def get_cart_by_user_id(self, user_id):
        query = 'select cart_id from "Cart" where user_id = %s;'
        cursor = self.conn.cursor()
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()[0]
        return result

    # Maybe this method should fetchone instead of returning
    def delete_cart(self, user_id):
        query = 'delete from "Cart" where user_id = %s'
        cursor = self.conn.cursor()
        cursor.execute(query, (user_id,))
        self.conn.commit()
        return user_id
