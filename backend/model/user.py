import psycopg2
from backend.config.dbconfig import dbconfig

class UserDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (dbconfig['database'],
                                                                            dbconfig['user'],
                                                                            dbconfig['password'],
                                                                            dbconfig['port'],
                                                                            dbconfig['host'])
        self.conn = psycopg2.connect(connection_url)

    def createNewUser(self, user_email, user_password, user_firstname,
                      user_lastname, user_phone, user_type):
        cursor = self.conn.cursor()
        query = 'insert into "User" (user_email, user_password, user_firstname, ' \
                'user_lastname, user_phone, user_type) values (%s,%s,%s,%s,%s,%s) returning user_id;'
        cursor.execute(query, (user_email, user_password, user_firstname, user_lastname,
                               user_phone, user_type))
        user_id = cursor.fetchone()[0]
        self.conn.commit()
        return user_id

    def updateWishlist(self, user_id, wishlist_id):
        cursor = self.conn.cursor()
        query = 'update "User" set wishlist_id = %s  where user_id = %s'
        cursor.execute(query, (wishlist_id, user_id,))
        self.conn.commit()
        return wishlist_id

    def checkEmails(self):
        cursor = self.conn.cursor()
        query = 'select user_email from "User"'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row[0])
        return result

    def login(self, user_email, user_password):
        cursor = self.conn.cursor()
        query = 'select user_id from "User" where user_email = %s and user_password = %s'
        cursor.execute(query, (user_email, user_password))
        user_id = cursor.fetchone()
        return user_id

    def getAllUsers(self):
        cursor = self.conn.cursor()
        query = 'select user_id, wishlist_id, user_email, user_password, user_firstname,  user_lastname, ' \
                'user_phone, user_type from "User"'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUserID(self, user_id):
        cursor = self.conn.cursor()
        query = 'select user_id, wishlist_id, user_email, user_password, user_firstname,  ' \
                'user_lastname, user_phone, user_type from "User" where user_id = %s'
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result

    def deleteUser(self, user_id):
        cursor = self.conn.cursor()
        query = 'delete from "User" where user_id = %s'
        cursor.execute(query, (user_id,))
        self.conn.commit()
        affected_rows = cursor.rowcount
        return affected_rows != 0

    def updateUser(self, user_id, user_email, user_password, user_firstname, user_lastname,
                   user_phone, user_type):
        cursor = self.conn.cursor()
        query = 'update "User" set user_email = %s, user_password = %s, user_firstname = %s, ' \
                'user_lastname = %s, user_phone = %s, user_type = %s where user_id = %s'
        cursor.execute(query, (user_email, user_password, user_firstname, user_lastname, user_phone,
                               user_type, user_id))
        self.conn.commit()
        query_show = 'select user_id, wishlist_id, user_email, user_password, user_firstname,  ' \
                     'user_lastname, user_phone, user_type from "User" where user_id = %s'
        cursor.execute(query_show, (user_id,))
        return cursor.fetchone()
        # affected_rows = cursor.rowcount
        # return affected_rows != 0

    # def addOrder(self, order_id, user_id):
    #     cursor = self.conn.cursor()
    #     query = 'update "User" set order_id = array_append(order_id, %s) where user_id = %s;'
    #     cursor.execute(query, (order_id, user_id))
    #     query_show = 'select order_id from "User" where user_id = %s'
    #     cursor.execute(query_show, (user_id,))
    #     result = cursor.fetchone()
    #     return result
    #
    # def deleteOrder(self, order_id, user_id):
    #     cursor = self.conn.cursor()
    #     query = 'update "User" set order_id = array_remove(order_id, %s) where user_id = %s;'
    #     query_show = 'select order_id from "User" where user_id = %s;'
    #     cursor.execute(query, (order_id, user_id))
    #     cursor.execute(query_show, (user_id,))
    #     result = cursor.fetchone()
    #     return result

    def highestProduct(self, user_id):
        cursor = self.conn.cursor()
        query = 'select product_id, product_name, product_price, product_dis, product_category from "Products" ' \
                'natural inner join (select product_id as id, max(product_price) as maximum from "Orders" ' \
                'natural inner join "Bought_Products" where user_id = %s group by product_id order by maximum desc ' \
                'fetch first row only) as result where result.id = product_id '
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result

    def lowestProduct(self, user_id):
        cursor = self.conn.cursor()
        query = 'select product_id, product_name, product_price, product_dis, product_category from "Products" ' \
                'natural inner join (select product_id as id, min(product_price) as minimum from "Orders" ' \
                'natural inner join "Bought_Products" where user_id = %s group by product_id order by minimum asc ' \
                'fetch first row only) as result where result.id = product_id '
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result

    def getRankingCategory(self, limit, user_id):
        cursor = self.conn.cursor()
        query = 'select p.product_name, sum(bp.product_quantity) as amount from "Orders" as oh natural inner join "Bought_Products" as bp inner join "Products" as p on p.product_id = bp.product_id where user_id = %s group by p.product_name order by amount desc limit 5'
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getRankingProduct(self, limit, user_id):
        cursor = self.conn.cursor()
        query = 'select bp.product_name, sum(bp.product_quantity) as amount from "Orders" as oh ' \
                'natural inner join "Bought_Products" as bp inner join "Products" as p on ' \
                'p.product_id = bp.product_id where user_id = %s group by bp.product_name order by amount desc limit %s'
        cursor.execute(query, (user_id, limit))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getType(self, user_id):
        cursor = self.conn.cursor()
        query = 'select user_type from "User" where user_id = %s'
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result
