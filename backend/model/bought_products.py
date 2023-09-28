from backend.config.dbconfig import dbconfig
import psycopg2


class BoughtProductsDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (dbconfig['database'],
                                                                            dbconfig['user'],
                                                                            dbconfig['password'],
                                                                            dbconfig['port'],
                                                                            dbconfig['host'])
        self.conn = psycopg2.connect(connection_url)

    def add_to_order_his(self, order_id, product_id, product_price, product_quantity, product_name):
        query = 'insert into "Bought_Products"(order_id, product_id, product_price, product_quantity, product_name) values ' \
                '(%s,%s,%s,%s,%s) returning order_id, product_id'
        cursor = self.conn.cursor()
        cursor.execute(query, (order_id, product_id, product_price, product_quantity, product_name))
        result = cursor.fetchone()
        self.conn.commit()
        return result

    def get_all(self, order_id):
        query = 'select order_id, product_id, product_price, product_quantity, product_name from "Bought_Products" where order_id = %s'
        cursor = self.conn.cursor()
        cursor.execute(query, (order_id,))
        result = cursor.fetchall()
        return result

    def delete_order(self, order_id):
        query = 'delete from "Bought_Products" where order_id = %s returning order_id'
        cursor = self.conn.cursor()
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()[0]
        self.conn.commit()
        return result

