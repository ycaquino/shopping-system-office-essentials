import psycopg2
from backend.config.dbconfig import dbconfig

class OrderDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (dbconfig['database'],
                                                                            dbconfig['user'],
                                                                            dbconfig['password'],
                                                                            dbconfig['port'],
                                                                            dbconfig['host'])
        self.conn = psycopg2.connect(connection_url)

    def get_all_orders(self):
        query = "select order_id, order_subtotal, order_tax, order_shipping, order_total, order_date, order_tracking, order_payment from orders"
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = []
        for record in cursor:
            result.append(record)
        return result

    def new_order(self, order_subtotal, order_tax, order_total, order_date, user_id):
        query = 'insert into "Orders"(order_subtotal, order_tax, order_total, order_date, user_id) values (%s,%s,%s,%s,%s) returning order_id;'
        cursor = self.conn.cursor()
        cursor.execute(query, (order_subtotal, order_tax, order_total, order_date, user_id))
        order_id = cursor.fetchone()[0]
        self.conn.commit()
        return order_id

    def delete_order(self, order_id):
        query = 'delete from "Orders" where order_id = %s returning order_id'
        cursor = self.conn.cursor()
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()[0]
        self.conn.commit()
        return result

    def get_order_total(self, order_id):
        query = 'select order_total from "Orders" where order_id = %s'
        cursor = self.conn.cursor()
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()[0]
        return result

    def get_order_by_id(self, order_id):
        query = 'select order_id, order_subtotal, order_tax, order_total, order_date from "Orders" where order_id = %s'
        cursor = self.conn.cursor()
        cursor.execute(query, (order_id,))
        result = cursor.fetchall()
        return result

    def get_all_orders(self):
        query = 'select order_id, order_subtotal, order_tax, order_total, order_date from "Orders"';
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_order_history_2(self, user_id):
        query = 'select order_id, product_name, product_price, product_quantity, order_subtotal,' \
                'order_tax, order_total, order_date from "Bought_Products" natural inner join "Orders" ' \
                'where user_id = %s'
        cursor = self.conn.cursor()
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_user_orders(self, user_id):
        query = 'select order_id from "Orders" natural inner join "User" where user_id = %s'
        cursor = self.conn.cursor()
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def delete_by_user_id(self, user_id):
        query = 'delete from "Orders" where user_id=%s returning user_id'
        cursor = self.conn.cursor()
        cursor.execute(query, (user_id, ))
        result = cursor.fetchone()
        self.conn.commit()
        return result

    def get_order_history(self, user_id):
        query = 'select order_id, order_subtotal, order_tax, order_total, order_date from "Orders" where user_id=%s'
        cursor = self.conn.cursor()
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result


