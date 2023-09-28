import psycopg2
from backend.config.dbconfig import dbconfig


class ProductDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (dbconfig['database'],
                                                                            dbconfig['user'],
                                                                            dbconfig['password'],
                                                                            dbconfig['port'],
                                                                            dbconfig['host'])
        self.conn = psycopg2.connect(connection_url)

    def checkIfDeletedHelper(self, product_id):
        cursor = self.conn.cursor()
        query = 'select active from "Products" where product_id = %s'
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()
        if not result[0]:
            return False
        return True

    def createProduct(self, product_name, product_price, product_dis, product_quantity, product_category,
                      user_id):
        cursor = self.conn.cursor()
        query_compare = 'select user_type from "User" where user_id = %s'
        cursor.execute(query_compare, (user_id,))
        if (cursor.fetchone()[0] == 'admin'):
            query = 'insert into "Products" (product_name, product_price, product_dis, product_quantity, product_category) values (%s,%s,%s,%s,%s) returning product_id;'
            cursor.execute(query,
                           (product_name, product_price, product_dis, product_quantity, product_category))
            product_id = cursor.fetchone()[0]
            self.conn.commit()
            return product_id
        else:
            return None

    def getAllProducts(self):
        cursor = self.conn.cursor()
        query = 'select product_id, product_name, product_price, product_dis, product_quantity, product_category, active from "Products" where active = true'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getProductID(self, product_id):
        cursor = self.conn.cursor()
        query = 'select product_id, product_name, product_price, product_dis, product_quantity, product_category, active from "Products" where product_id = %s and active = true'
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()
        return result

    def deleteProduct(self, product_id, user_id):
        cursor = self.conn.cursor()
        user_type = 'admin'
        query = 'update "Products" set active = false from "User"' \
                'where user_type = %s and user_id = %s and product_id = %s;'
        cursor.execute(query, (user_type, user_id, product_id))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows != 0

    def updateProduct(self, product_id, product_name, product_price, product_dis, product_quantity, product_category, active,user_id):
        cursor = self.conn.cursor()
        user_type = 'admin'
        query = 'update "Products" set product_id = %s, product_name = %s,  product_price = %s, product_dis = %s, product_quantity = %s, product_category = %s, active = %s from "User" where user_id=%s and user_type=%s and product_id = %s'
        cursor.execute(query, (
        product_id, product_name, product_price, product_dis, product_quantity, product_category, active, user_id,
        user_type, product_id))
        self.conn.commit()
        query_show = 'select product_id, product_name, product_price, product_dis, product_quantity, product_category, active from "Products" where product_id = %s'
        cursor.execute(query_show, (product_id,))
        return cursor.fetchone()

    def updateProductPrice(self, product_id, product_price, user_id):
        cursor = self.conn.cursor()
        user_type = 'admin'
        query = 'Update "Products" set product_price = %s from "User" ' \
                'where user_type = %s and user_id = %s and product_id = %s;'
        cursor.execute(query, (product_price, user_type, user_id, product_id))
        query_show = 'select product_id, product_name, product_price, product_dis, product_quantity, product_category, active from "Products" where product_id = %s'
        cursor.execute(query_show, (product_id,))
        self.conn.commit()
        return cursor.fetchone()

    def updateProductQuantity(self, product_id, product_quantity, user_id):
        cursor = self.conn.cursor()
        user_type = 'admin'
        query = 'update "Products" set product_quantity = %s from "User" ' \
                'where user_type = %s and user_id = %s and product_id = %s;'
        cursor.execute(query, (product_quantity, user_type, user_id, product_id))
        query_show = 'select product_id, product_name, product_price, product_dis, product_quantity, product_category, active from "Products" where product_id = %s'
        cursor.execute(query_show, (product_id,))
        self.conn.commit()
        return cursor.fetchone()

    def getProductByCategory(self, product_category):
        cursor = self.conn.cursor()
        query = 'select product_id, product_name, product_price, product_dis, product_quantity, product_category, active from "Products" where product_category = %s and active = true'
        cursor.execute(query, (product_category,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getProductByName(self, product_name):
        cursor = self.conn.cursor()
        query = 'select product_id, product_name, product_price, product_dis, product_quantity, product_category, active from "Products" where product_name = %s and active = true'
        cursor.execute(query, (product_name,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getProductNameInAscendingOrder(self):
        cursor = self.conn.cursor()
        query = 'select product_id, product_name, product_price, product_dis, product_quantity, product_category, active from "Products" where active = true order by product_name asc'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getProductNameInDescendingOrder(self):
        cursor = self.conn.cursor()
        query = 'select product_id, product_name, product_price, product_dis, product_quantity, product_category, active from "Products" where active = true order by product_name desc'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getProductByPrice(self, product_price):
        cursor = self.conn.cursor()
        query = 'select product_id, product_name, product_price, product_dis, product_quantity, product_category, active from "Products" where product_price = %s and active = true'
        cursor.execute(query, (product_price,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getProductPriceInAscendingOrder(self):
        cursor = self.conn.cursor()
        query = 'select product_id, product_name, product_price, product_dis, product_quantity, product_category, active from "Products" where active = true order by product_price asc'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getProductPriceInDescendingOrder(self):
        cursor = self.conn.cursor()
        query = 'select product_id, product_name, product_price, product_dis, product_quantity, product_category, active from "Products" where active = true order by product_price desc'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    # Global Stats

    def getProductMostExpensive(self):
        cursor = self.conn.cursor()
        query = 'select product_id, product_name, product_price, product_dis, product_quantity, product_category, active from "Products" ' \
                'order by product_price desc limit 1'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getProductLeastExpensive(self):
        cursor = self.conn.cursor()
        query = 'select product_id, product_name, product_price, product_dis, product_quantity, product_category, active from "Products" ' \
                'order by product_price asc limit 1'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getGlobalRankingProducts(self, limit):
        cursor = self.conn.cursor()
        query = 'select product_name, sum(product_quantity) from "Bought_Products" ' \
                'group by product_name order by sum(product_quantity) desc limit %s'
        cursor.execute(query, (limit,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getGlobalRankingCategories(self, limit):
        cursor = self.conn.cursor()
        query = 'select p.product_category, sum(bp.product_quantity) from "Products" as p ' \
                'inner join "Bought_Products" as bp on p.product_id = bp.product_id ' \
                'group by p.product_category order by sum(bp.product_quantity) desc limit %s'
        cursor.execute(query, (limit,))
        result = []
        for row in cursor:
            result.append(row)
        return result
