from flask import jsonify

from backend.model.product import ProductDAO
from backend.model.wishlist import WishlistDAO


def build_wishlist_map_dic(row):
    result = {
        'wishlist_id': row[0], 'user_id': row[1], 'product_id': row[2]
    }
    return result


def build_most_liked_product(row):
    result = {
        'product_id': row[0],
        'product_name': row[1],
        'product_price': row[2],
        'product_dis': row[3],
        'product_category': row[4]
    }
    return result


class BaseWishlist:

    def deleteExistingWishlist(self, wishlist_id):
        wishlist_dao = WishlistDAO()
        wishlist = wishlist_dao.deleteExistingWishlist(wishlist_id)
        if wishlist:
            return jsonify("Wishlist deleted"), 200
        else:
            return jsonify("Error deleting Wishlist"), 409

    def getAllWishlists(self):
        wishlist_dao = WishlistDAO()
        wishlists_lists = wishlist_dao.getAllWishlists()
        result = []
        for row in wishlists_lists:
            obj = build_wishlist_map_dic(row)
            result.append(obj)
        return jsonify(result), 200

    def getWishlistID(self, wishlist_id):
        wishlist_dao = WishlistDAO()
        wishlist = wishlist_dao.getWishlistID(wishlist_id)
        if not wishlist:
            return jsonify("Wishlist doesn't EXIST"), 404
        result = []
        for row in wishlist:
            obj = build_wishlist_map_dic(row)
            result.append(obj)
        return jsonify(result), 200

    def getWishlistbyUser(self, user_id):
        wishlist_dao = WishlistDAO()
        wishlist_id = wishlist_dao.getWishlistWithUser(user_id)
        wishlist = wishlist_dao.getWishlistID(wishlist_id)
        products = []
        for row in wishlist:
            products.append(row[2])

        product_dao = ProductDAO()
        result = [wishlist_id]
        for items in products:
            result.append(product_dao.getProductID(items))
        return jsonify(result), 200

    def getMostLiked(self):
        wishlist_dao = WishlistDAO()
        mostLiked = wishlist_dao.getMostLiked()
        result = build_most_liked_product(mostLiked)
        return jsonify(result), 200
