from flask import jsonify
from backend.model.product import ProductDAO


def build_product_map_dic(row):
    result = {
        'product_id': row[0],
        'product_name': row[1],
        'product_price': row[2],
        'product_dis': row[3],
        'product_quantity': row[4],
        'product_category': row[5],
        'active': row[6]
    }
    return result

def build_product_attribute_dic(product_id, product_name, product_price, product_dis, product_quantity, product_category, active):
    result = {
        'product_id': product_id,
        'product_name': product_name,
        'product_price': product_price,
        'product_dis': product_dis,
        'product_quantity': product_quantity,
        'product_category': product_category,
        'active': active
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

class ProductController:
    def createProduct(self, json):
        product_dao = ProductDAO()
        product_name = json["product_name"]
        product_price = json["product_price"]
        product_dis = json["product_dis"]
        product_quantity = json["product_quantity"]
        product_category = json["product_category"]
        # active = json["active"]
        user_id = json["user_id"]
        product_id = product_dao.createProduct(product_name, product_price, product_dis, product_quantity, product_category, user_id)
        result = build_product_attribute_dic(product_id, product_name, product_price, product_dis, product_quantity, product_category, True)
        return jsonify(result), 201

    def updateProduct(self, product_id, json):
        product_dao = ProductDAO()
        product_name = json["product_name"]
        product_price = json["product_price"]
        product_dis = json["product_dis"]
        product_quantity = json["product_quantity"]
        product_category = json["product_category"]
        active = json["active"]
        user_id = json["user_id"]
        product_updated = product_dao.updateProduct(product_id, product_name, product_price, product_dis, product_quantity, product_category, active, user_id)
        if not product_updated:
            return jsonify("Product does not exist"), 404
        result = build_product_map_dic(product_updated)
        return jsonify(result), 200

    # for frontEnd
    def updateProductByUserId(self, product_id, product_name, product_price, product_dis, product_quantity, product_category, user_id):
        product_dao = ProductDAO()
        product_updated = product_dao.updateProductByUserId(product_id, product_name, product_price, product_dis, product_quantity, product_category, user_id)
        if not product_updated:
            return jsonify("Product does not exist"), 404
        result = build_product_map_dic(product_updated)
        return jsonify(result), 200

    def updateProductPrice(self, product_id, json):
        product_dao = ProductDAO()
        product_price = json["product_price"]
        user_id = json["user_id"]
        product_updated = product_dao.updateProductPrice(product_id, product_price, user_id)
        if not product_updated:
            return jsonify("Product does not exist"), 404
        result = build_product_map_dic(product_updated)
        return jsonify(result), 200

    def updateProductQuantity(self, product_id, json):
        product_dao = ProductDAO()
        product_quantity = json["product_quantity"]
        user_id = json["user_id"]
        product_updated = product_dao.updateProductQuantity(product_id, product_quantity, user_id)
        if not product_updated:
            return jsonify("Product does not exist"), 404
        result = build_product_map_dic(product_updated)
        return jsonify(result), 200

    def getAllProducts(self):
        product_dao = ProductDAO()
        product_list = product_dao.getAllProducts()
        result = []
        for row in product_list:
            obj = build_product_map_dic(row)
            result.append(obj)

        return jsonify(result), 200

    def getProductID(self, product_id):
        product_dao = ProductDAO()
        product = product_dao.getProductID(product_id)
        helper = product_dao.checkIfDeletedHelper(product_id)
        if not product or not helper:
            return jsonify("Product does not exist"), 404
        result = build_product_map_dic(product)
        return jsonify(result), 200

    def deleteProduct(self, product_id, json):
        product_dao = ProductDAO()
        user_id = json["user_id"]
        delete_product = product_dao.deleteProduct(product_id, user_id)
        if not delete_product:
            return jsonify("Product does not exist"), 404
        return jsonify(delete_product), 200

    def deleteProductUserId(self, product_id, user_id): #for frontEnd
        product_dao = ProductDAO()
        delete_product = product_dao.deleteProduct(product_id, user_id)
        if not delete_product:
            return jsonify("Product does not exist"), 404
        return jsonify(delete_product), 200

    def getProductByCategory(self, product_category):
        product_dao = ProductDAO()
        product_list = product_dao.getProductByCategory(product_category)
        result = []
        for row in product_list:
            obj = build_product_map_dic(row)
            result.append(obj)

        return jsonify(result), 200

    def getProductByName(self, product_name):
        product_dao = ProductDAO()
        product_list = product_dao.getProductByName(product_name)
        result = []
        for row in product_list:
            obj = build_product_map_dic(row)
            result.append(obj)

        return jsonify(result), 200

    def getProductNameByOrder(self, order):
        product_dao = ProductDAO()
        if(order == "asc"):
            product_list = product_dao.getProductNameInAscendingOrder()
        elif(order == "desc"):
            product_list = product_dao.getProductNameInDescendingOrder()
        result = []
        for row in product_list:
            obj = build_product_map_dic(row)
            result.append(obj)

        return jsonify(result), 200

    def getProductByPrice(self, product_price):
        product_dao = ProductDAO()
        product_list = product_dao.getProductByPrice(product_price)
        result = []
        for row in product_list:
            obj = build_product_map_dic(row)
            result.append(obj)

        return jsonify(result), 200

    def getProductPriceByOrder(self, order):
        product_dao = ProductDAO()
        if(order == "asc"):
            product_list = product_dao.getProductPriceInAscendingOrder()
        elif(order == "desc"):
            product_list = product_dao.getProductPriceInDescendingOrder()
        result = []
        for row in product_list:
            obj = build_product_map_dic(row)
            result.append(obj)

        return jsonify(result), 200

    # helper method for add to cart and order op
    def get_product_by_id(self, product_id):
        product_dao = ProductDAO()
        product = product_dao.getProductID(product_id)
        if not product:
            return jsonify("Product does not exist"), 404
        result = build_product_map_dic(product)
        return result

    # stats

    def getProductMostExpensive(self):
        product_dao = ProductDAO()
        product_list = product_dao.getProductMostExpensive()
        result = []
        for row in product_list:
            obj = build_product_map_dic(row)
            result.append(obj)

        return jsonify(result), 200

    def getProductLeastExpensive(self):
        product_dao = ProductDAO()
        product_list = product_dao.getProductLeastExpensive()
        result = []
        for row in product_list:
            obj = build_product_map_dic(row)
            result.append(obj)

        return jsonify(result), 200

    def getGlobalRankingProducts(self, limit):

        product_dao = ProductDAO()
        ranking_result = product_dao.getGlobalRankingProducts(limit)
        if not ranking_result:
            return jsonify("Has not quantity needed"), 404
        result = []
        for row in ranking_result:
            result.append(build_ranking_category_dic(row))
        return jsonify(result), 200

    def getGlobalRankingCategories(self, limit):

        product_dao = ProductDAO()
        ranking_result = product_dao.getGlobalRankingCategories(limit)
        if not ranking_result:
            return jsonify("Has not quantity needed"), 404
        result = []
        for row in ranking_result:
            result.append(build_ranking_category_dic(row))
        return jsonify(result), 200


