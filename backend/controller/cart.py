from flask import jsonify
from backend.model.cart import CartDAO

class CartController:

    def build_dict(self, row):
        result = {}
        result['CartId'] = row[0]
        result['UserId'] = row[1]
        return result

    def create_cart(self, user_id):
        dao = CartDAO()
        cart_id = dao.create_cart(user_id)
        return cart_id

    def get_all_carts(self):
        dao = CartDAO()
        result_tuples = dao.get_all_carts()
        result = []
        for row in result_tuples:
            result.append(self.build_dict(row))
        return jsonify(result)

    def get_cart_by_id(self, cart_id):
        dao = CartDAO()
        result = dao.get_cart_by_id(cart_id)
        if result:
            return result, 200
        return jsonify('Cart not found.'), 404

    def get_cart_by_user_id(self, user_id):
        dao = CartDAO()
        result = dao.get_cart_by_user_id(user_id)
        if result:
            return result, 200
        return jsonify('Cart not found.'), 404

    def delete_cart(self, user_id):
        dao = CartDAO()
        result = dao.delete_cart(user_id)
        if result:
            return jsonify(result), 200
        return jsonify('User not found'), 404