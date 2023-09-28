from flask import jsonify
from backend.model.wishlist import WishlistDAO
from backend.model.wishlist_contents import WishlistContentsDAO

def build_wishlist_map_dic(row):
    result = {
        'wishlist_id': row[0], 'user_id': row[1], 'product_id': row[2]
    }
    return result


class BaseWishlistContents:

    def addProductInWishlist(self, wishlist_id, product_id):
        wishlist_dao = WishlistDAO()
        wishlist_contents_dao = WishlistContentsDAO()
        wishlist = wishlist_dao.verifyWishlistID(wishlist_id)
        if not wishlist:
            return jsonify("Wishlist doesn't EXIST"), 404
        if wishlist_contents_dao.verifyExistingProductInWishList(wishlist_id, product_id) is None:
            wishlist_contents_dao.addProductInWishlist(wishlist_id, product_id)
            wishlist = wishlist_dao.getWishlistID(wishlist_id)
            result = []
            for row in wishlist:
                result.append(build_wishlist_map_dic(row))
            return jsonify(result), 200
        else:
            return jsonify("Product is in the Wishlist"), 409

    def deleteProductInWishlist(self, wishlist_id, product_id):
        wishlist_dao = WishlistDAO()
        wishlist_contents_dao = WishlistContentsDAO()
        wishlist = wishlist_dao.verifyWishlistID(wishlist_id)
        if not wishlist:
            return jsonify("Wishlist doesn't EXIST"), 404
        if wishlist_contents_dao.verifyExistingProductInWishList(wishlist_id, product_id) is not None:
            wishlist_contents_dao.deleteProductInWishlist(wishlist_id, product_id)
            return jsonify("Product Deleted"), 200
        else:
            return jsonify("Product is not in the Wishlist"), 409
