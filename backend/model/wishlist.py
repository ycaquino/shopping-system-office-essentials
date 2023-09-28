import psycopg2

from backend.config.dbconfig import dbconfig


class WishlistDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (dbconfig['database'],
                                                                            dbconfig['user'],
                                                                            dbconfig['password'],
                                                                            dbconfig['port'],
                                                                            dbconfig['host'])
        self.conn = psycopg2.connect(connection_url)

    def createNewWishlist(self, user_id):
        cursor = self.conn.cursor()
        query = 'insert into "Wishlist" (user_id) values (%s) returning wishlist_id;'
        cursor.execute(query, (user_id,))
        wishlist_id = cursor.fetchone()[0]
        self.conn.commit()
        return wishlist_id

    def deleteExistingWishlist(self, wishlist_id):
        cursor = self.conn.cursor()
        query = 'delete from "Wishlist" where wishlist_id=%s'
        cursor.execute(query, (wishlist_id,))
        self.conn.commit()
        affected_rows = cursor.rowcount
        return affected_rows != 0


    def getMostLiked(self):
        cursor = self.conn.cursor()
        query = 'select product_id, product_name, product_price, product_dis, product_category from "Products" ' \
                'natural inner join ( select product_id, count(product_id) as frequency from "Wishlist_Contents"' \
                ' group by product_id order by frequency desc fetch first row only) as result ' \
                'where result.product_id = product_id'
        cursor.execute(query, ())
        result = cursor.fetchone()
        return result

    def getAllWishlists(self):
        cursor = self.conn.cursor()
        query = 'select * from "Wishlist" natural inner join "Wishlist_Contents" order by wishlist_id'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getWishlistID(self, wishlist_id):
        cursor = self.conn.cursor()
        query = 'select * from "Wishlist" natural inner join "Wishlist_Contents" where wishlist_id = %s'
        cursor.execute(query, (wishlist_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def verifyWishlistID(self, wishlist_id):
        cursor = self.conn.cursor()
        query = 'select * from "Wishlist" where wishlist_id = %s'
        cursor.execute(query, (wishlist_id,))
        result = cursor.fetchone()
        return result

    def getWishlistWithUser(self, user_id):
        cursor = self.conn.cursor()
        query = 'select wishlist_id from "Wishlist" where user_id = %s'
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result
