from flask import jsonify
from backend.model.user import UserDAO
from backend.model.wishlist import WishlistDAO
from backend.controller.cart import CartController


def build_user_map_dic(row):
    result = {
        'user_id': row[0], 'wishlist_id': row[1],
        'user_email': row[2], 'user_password': row[3],
        'user_firstname': row[4], 'user_lastname': row[5], 'user_phone': row[6],
        'user_type': row[7]
    }
    return result


def build_user_attribute_dic(user_id, wishlist_id, user_email, user_password, user_firstname, user_lastname,
                             user_phone, user_type):
    result = {
        'user_id': user_id, 'wishlist_id': wishlist_id,
        'user_email': user_email, 'user_password': user_password,
        'user_firstname': user_firstname, 'user_lastname': user_lastname, 'user_phone': user_phone,
        'user_type': user_type
    }
    return result


def build_ranking_category_dic(row):
    result = {
        'product_category': row[0], 'count': row[1]
    }
    return result


def build_ranking_product_dic(row):
    result = {
        'product_name': row[0], 'amount': row[1]
    }
    return result

def build_product_dic(row):
    result = {
        'product_id': row[0], "product_name": row[1], 'product_price': row[2], 'product_dis': row[3], 'product_category': row[4]
    }
    return result


class BaseUser:
    def createUser(self, json):
        user_dao = UserDAO()
        user_email = json["user_email"]
        emails = user_dao.checkEmails()
        if user_email in emails:
            return [1], 404
        user_password = json["user_password"]
        user_firstname = json["user_firstname"]
        user_lastname = json["user_lastname"]
        user_phone = json["user_phone"]
        user_type = json["user_type"]

        user_id = user_dao.createNewUser(user_email, user_password, user_firstname,
                                         user_lastname, user_phone, user_type)
        wishlist_id = WishlistDAO().createNewWishlist(user_id)
        user_dao.updateWishlist(user_id, wishlist_id)
        result = build_user_attribute_dic(user_id, wishlist_id, user_email, user_password, user_firstname,
                                          user_lastname, user_phone, user_type)
        return result, 201

    def login(self, json):
        user_email = json['user_email']
        user_password = json["user_password"]
        user_dao = UserDAO()
        user_id = user_dao.login(user_email, user_password)
        return jsonify(user_id), 200


    def updateUser(self, json):
        # cart_id = json["cart_id"]
        # order_id = json["order_id"]
        # wishlist_id = json["wishlist_id"]
        user_id = json["user_id"]
        user_email = json["user_email"]
        user_password = json["user_password"]
        user_firstname = json["user_firstname"]
        user_lastname = json["user_lastname"]
        user_phone = json["user_phone"]
        user_type = json["user_type"]

        user_dao = UserDAO()
        updated = user_dao.updateUser(user_id, user_email, user_password, user_firstname, user_lastname,
                                      user_phone, user_type)
        if updated:
            return jsonify(updated), 200
        else:
            return jsonify("User not found"), 404

    def getAllUsers(self):
        user_dao = UserDAO()
        users_list = user_dao.getAllUsers()
        result = []
        for row in users_list:
            obj = build_user_map_dic(row)
            result.append(obj)

        return jsonify(result), 200

    def getUserID(self, json):
        user_dao = UserDAO()
        user_id = json["user_id"]
        user = user_dao.getUserID(user_id)
        if not user:
            return jsonify("User does not exist"), 404
        result = build_user_map_dic(user)
        return jsonify(result), 200

    def deleteUser(self, json):
        user_dao = UserDAO()
        user_id = json["user_id"]
        CartController().delete_cart(user_id)
        user_deleted = user_dao.deleteUser(user_id)
        if not user_deleted:
            return jsonify("User does not exist"), 404
        else:
            return jsonify("User has been deleted"), 200

    # def addOrder(self, order_id, user_id):
    #     user_dao = UserDAO()
    #     orders = user_dao.addOrder(order_id, user_id)
    #     if not orders:
    #         return jsonify("User does not exist"), 404
    #     return jsonify(orders), 200
    #
    # def deleteOrder(self, order_id, user_id):
    #     user_dao = UserDAO()
    #     delete_orders = user_dao.deleteOrder(order_id, user_id)
    #     if not delete_orders:
    #         return jsonify("User or order does not exist"), 404
    #     return jsonify(delete_orders), 200

    def highestProduct(self, json):
        user_dao = UserDAO()
        user_id = json["user_id"]
        highest = user_dao.highestProduct(user_id)
        if not highest:
            return jsonify("User does not exist or has not made any orders"), 404
        result = build_product_dic(highest)
        return jsonify(result), 200

    def lowestProduct(self, json):
        user_dao = UserDAO()
        user_id = json["user_id"]
        lowest = user_dao.lowestProduct(user_id)
        if not lowest:
            return jsonify("User does not exist or has not made any orders"), 404
        result = build_product_dic(lowest)
        return jsonify(result), 200

    def getRankingCategory(self, limit, json):
        user_dao = UserDAO()
        user_id = json["user_id"]
        ranking_result = user_dao.getRankingCategory(limit, user_id)
        if not ranking_result:
            return jsonify("User does not exist or has not made any orders"), 404
        result = []
        for row in ranking_result:
            result.append(build_ranking_category_dic(row))
        return jsonify(result), 200

    def getRankingProduct(self, limit, json):
        user_dao = UserDAO()
        user_id = json["user_id"]
        ranking_result = user_dao.getRankingProduct(limit, user_id)
        if not ranking_result:
            return jsonify("User does not exist or has not made any orders"), 404
        result = []
        for row in ranking_result:
            result.append(build_ranking_product_dic(row))
        return jsonify(result), 200

    def getType(self, user_id):
        user_dao = UserDAO()
        user_type = user_dao.getType(user_id)
        return jsonify(user_type), 200


