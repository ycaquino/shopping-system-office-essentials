import psycopg2

from backend.config.dbconfig import dbconfig


class WishlistContentsDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (dbconfig['database'],
                                                                            dbconfig['user'],
                                                                            dbconfig['password'],
                                                                            dbconfig['port'],
                                                                            dbconfig['host'])
        self.conn = psycopg2.connect(connection_url)

    def deleteProductInWishlist(self, wishlist_id, product_id):
        cursor = self.conn.cursor()
        query = 'delete from "Wishlist_Contents" where product_id = %s and wishlist_id = %s;'
        cursor.execute(query, (product_id, wishlist_id,))
        self.conn.commit()
        affected_rows = cursor.rowcount
        return affected_rows != 0

    def addProductInWishlist(self, wishlist_id, product_id):
        cursor = self.conn.cursor()
        query = 'insert into "Wishlist_Contents" (product_id, wishlist_id) values (%s,%s);'
        cursor.execute(query, (product_id, wishlist_id,))
        self.conn.commit()
        affected_rows = cursor.rowcount
        return affected_rows != 0

    def verifyExistingProductInWishList(self, wishlist_id, product_id):
        cursor = self.conn.cursor()
        query = 'select * from "Wishlist_Contents" where product_id = %s and wishlist_id = %s;'
        cursor.execute(query, (product_id, wishlist_id,))
        existing_product = cursor.fetchone()
        return existing_product
