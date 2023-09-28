from flask import Flask, request, jsonify
from flask_cors import CORS

from backend.controller.user import BaseUser
from backend.controller.wishlist import BaseWishlist
from backend.controller.wishlist_contents import BaseWishlistContents
from backend.controller.order import OrderController
from backend.controller.cart import CartController
from backend.controller.cart_contents import CartContentsController
from backend.controller.bought_products import BoughtProductsController
from backend.controller.product import ProductController

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['GET'])
def introduction():
    return "Welcome to Office Essentials"


#####################################################################
#                             User                                  #
#####################################################################
@app.route("/office-essentials/User/all", methods=['GET', 'POST'])
def handleAllUsers():
    if request.method == 'GET':
        return BaseUser().getAllUsers()
    elif request.method == 'POST':
        user = BaseUser().createUser(request.json)
        if user[1] == 404:
            return jsonify(0), 200
        else:
            user_id = user[0]['user_id']
            CartController().create_cart(user_id)
            return jsonify(user), 201
    else:
        return jsonify("Method does not exist"), 405


@app.route("/office-essentials/User/id/", methods=['PUT', 'DELETE', 'POST'])
def handleUserByID():
    if request.method == 'PUT':
        return BaseUser().getUserID(request.json)
    elif request.method == 'DELETE':
        return BaseUser().deleteUser(request.json)
    elif request.method == 'POST':
        return BaseUser().updateUser(request.json)
    else:
        return jsonify("Method does not exist"), 405

@app.route("/office-essentials/User/login/", methods=['PUT'])
def login():
    if request.method == 'PUT':
        return BaseUser().login(request.json)
    else:
        return jsonify('Method does not exist'), 405


# @app.route("/office-essentials/User/Order/<int:user_id>/<int:order_id>", methods=['GET', 'DELETE'])
# def addOrdersWithUser(order_id, user_id):
#     if request.method == 'GET':
#         return BaseUser().addOrder(order_id, user_id)
#     elif request.method == 'DELETE':
#         return BaseUser().deleteOrder(order_id, user_id)
#     else:
#         return jsonify("Method does not exist"), 405


@app.route("/office-essentials/User/HighestProduct/", methods=['POST'])
def getHighestProduct():
    if request.method == 'POST':
        return BaseUser().highestProduct(request.json)
    else:
        return jsonify('Method does not exist'), 405


@app.route("/office-essentials/User/LowestProduct/", methods=['POST'])
def getLowestProduct():
    if request.method == 'POST':
        return BaseUser().lowestProduct(request.json)
    else:
        return jsonify('Method does not exist'), 405


@app.route("/office-essentials/User/RankingCategories/<int:limit>", methods=['POST'])
def getRankingCategories(limit):
    if request.method == 'POST':
        return BaseUser().getRankingCategory(limit, request.json)
    else:
        return jsonify('Method does not exist'), 405


@app.route("/office-essentials/User/RankingProduct/<int:limit>", methods=['POST'])
def getRankingProducts(limit):
    if request.method == 'POST':
        return BaseUser().getRankingProduct(limit, request.json)
    else:
        return jsonify('Method does not exist'), 405

@app.route("/office-essentials/User/Type/<int:user_id>", methods=['GET'])
def getType(user_id):
    if request.method == 'GET':
        return BaseUser().getType(user_id)
    else:
        return jsonify('Method does not exist'), 405

#---------------------------------------------------------------------------------
# Wishlist
#---------------------------------------------------------------------------------

@app.route("/office-essentials/Wishlist/all", methods=['GET'])
def handleAllWishlists():
    if request.method == 'GET':
        return BaseWishlist().getAllWishlists()
    else:
        return jsonify("Method Not Allowed"), 405

@app.route("/office-essentials/Wishlist/id/<int:wishlist_id>", methods=['GET', 'DELETE'])
def handleWishListByID(wishlist_id):
    if request.method == 'DELETE':
        return BaseWishlist().deleteExistingWishlist(wishlist_id)
    elif request.method == 'GET':
        return BaseWishlist().getWishlistID(wishlist_id)
    else:
        return jsonify("Method Not allowed"), 405

@app.route("/office-essentials/Wishlist/<int:wishlist_id>/<int:product_id>", methods=['GET', 'DELETE'])
def addInWishlist(wishlist_id, product_id):
    if request.method == 'GET':
        return BaseWishlistContents().addProductInWishlist(wishlist_id, product_id)
    elif request.method == 'DELETE':
        return BaseWishlistContents().deleteProductInWishlist(wishlist_id, product_id)
    else:
        return jsonify("Method does not exist"), 405

@app.route("/office-essentials/Wishlist/MostLiked", methods=['GET'])
def mostLiked():
    if request.method == 'GET':
        return BaseWishlist().getMostLiked()
    else:
        return jsonify("Method does not exist"), 405


@app.route("/office-essentials/Wishlist/<int:user_id>", methods=['GET'])
def getWishlistByUser(user_id):
    if request.method == 'GET':
        return BaseWishlist().getWishlistbyUser(user_id)
    else:
        return jsonify("Method does not exist"), 405


#####################################################################
#                             Cart                                  #
#####################################################################

@app.route("/office-essentials/CartContents", methods=['POST', 'DELETE'])
def alter_cart():
    if request.method == 'POST':
        return CartContentsController().add_to_cart(request.json)
    elif request.method == 'DELETE':
        cart_contents = CartContentsController().remove_from_cart(request.json)
        return jsonify(cart_contents[0]), cart_contents[1]
    return jsonify(Error='Method not allowed'), 405

@app.route("/office-essentials/Cart/<int:user_id>", methods=['GET'])
def get_cart_by_id(user_id):
    if request.method == 'GET':
        return jsonify(CartController().get_cart_by_user_id(user_id))
    else:
        return jsonify(Error='Method not allowed'), 405


@app.route("/office-essentials/CartContents/clear", methods=['DELETE'])
def clear_cart():
    if request.method == 'DELETE':
        cart_id = request.json['CartId']
        return CartContentsController().remove_all(cart_id)
    return jsonify(Error='Method not allowed'), 405

@app.route("/office-essentials/CartContents/getallfromcart/<int:cart_id>")
def get_all_from_cart(cart_id):
    if request.method == 'GET':
        cart_contents = CartContentsController().get_all_from_cart(cart_id)

        # cart not found
        if cart_contents[1] == 404:
            return cart_contents

        # cart is empty
        elif cart_contents[1] == 400:
            return cart_contents

        # cart contents
        else:
            return jsonify(cart_contents[0]), cart_contents[1]
    return jsonify(Error='Method not allowed'), 405


@app.route("/office-essentials/CartContents/getsubtotal/<int:cart_id>", methods=['GET'])
def get_subtotal(cart_id):
    if request.method == 'GET':
        return CartContentsController().calculate_subtotal(cart_id)
    return jsonify(Error='Method not allowed'), 405


#####################################################################
#                             Order                                 #
#####################################################################

@app.route("/office-essentials/Orders/neworder", methods=['POST'])
def new_order():
    if request.method == 'POST':
        # get the user_id and check if user exists
        user_id = request.json['user_id']
        is_user = BaseUser().getUserID(request.json)
        if is_user[1] == 404:
            return is_user

        # get the cart associated with that user
        cart_id = CartController().get_cart_by_user_id(user_id)[0]

        # get the products from the cart and for every product on the cart calculate the price
        # this is a list of dictionaries whit the information that is inside the table
        cart_contents = CartContentsController().get_all_from_cart(cart_id)
        if cart_contents[1] == 404:
            return jsonify('Your order could not be processed at the time because you cart is empty. '
                           'Please add some products and try again.'), 400

        cart_subtotal = 0
        out_of_stock = False

        for product in cart_contents[0]:
            #print(product)
            # get product info first
            # this a dictionary with all the product info
            product_info = ProductController().get_product_by_id(product['ProductId'])
            product_id = product_info['product_id']
            #print(product_info)
            # calculate sub_total
            if not(product_info['product_quantity'] >= product['ProductQuantity']):
                #delete product from cart
                CartContentsController().delete_all_from_cart(cart_id=cart_id, product_id=product_id)
                out_of_stock = True
            product_price = product_info['product_price'] * (1 - product_info['product_dis'])
            product_price = round(product_price, 2)
            cart_subtotal = cart_subtotal + (product_price * product['ProductQuantity'])

        if out_of_stock:
            return jsonify('The stock of one or more items has changed. Please try again.', 403)
        # cart_subtotal = round(cart_subtotal - 0.005, 2)
        #print(cart_subtotal)

        # create the order
        order_id = OrderController().new_order(cart_subtotal, user_id)
        order_info = OrderController().get_order_by_id(order_id)[0][0]
        #print(order_info)
        order_tax = order_info['order_tax']
        order_total = order_info['order_total']
        order_date = order_info['order_date']
        order_subtotal = order_info['order_subtotal']

        # move the items from Cart_Contents to Bought_Products
        for product in cart_contents[0]:
            product_info = ProductController().get_product_by_id(product['ProductId'])
            product_id = product_info['product_id']
            product_price = round((product_info['product_price'] * (1 - product_info['product_dis'])), 2)
            product_quantity = product['ProductQuantity']
            product_name = product_info['product_name']
            BoughtProductsController().add_to_order_his(order_id, product_id, product_price, product_quantity, product_name)
            json = {'product_name': product_info['product_name'],
                    'product_price': product_info['product_price'],
                    'product_dis': product_info['product_dis'],
                    'product_quantity': product_info['product_quantity'] - product['ProductQuantity'],
                    'product_category': product_info['product_category'],
                    'active': product_info['active'],
                    'user_id': 106
                    }
            # get products out of inventory
            ProductController().updateProduct(product_id, json)

        # clear cart contents
        CartContentsController().remove_all(cart_id)

        return jsonify(BoughtProductsController().receipt(order_id, order_subtotal, order_tax, order_total, order_date)), 201

    return jsonify(Error='Method not allowed'), 405

@app.route("/office-essentials/Order/deleteorder", methods=['DELETE'])
def delete_order():
    if request.method == 'DELETE':
        order_id = request.json['OrderId']
        if OrderController().get_order_by_id(order_id)[1] == 404:
            return jsonify('Order not found.'), 404
        BoughtProductsController().delete_order(order_id)
        return OrderController().delete_order(order_id)
    else:
        jsonify(Error='Method not allowed'), 405


@app.route("/office-essentials/Orders/getorderbyid/<int:order_id>")
def get_order_by_id(order_id):
    if request.method == 'GET':
        if OrderController().get_order_by_id(order_id)[1] == 404:
            return jsonify('Order not found'), 404
        order_info = OrderController().get_order_by_id(order_id)[0][0]
        order_subtotal = order_info['order_subtotal']
        order_tax = order_info['order_tax']
        order_total = order_info['order_total']
        order_date = order_info['order_date']
        return jsonify(BoughtProductsController().receipt(order_id, order_subtotal, order_tax, order_total, order_date)), 200
    return jsonify(Error='Method not allowed'), 405

@app.route("/office-essentials/Orders/orderhistory2", methods=['GET','POST'])
def order_history_2():
    if request.method == 'POST':
        user_id = request.json['user_id']
        is_user = BaseUser().getUserID(request.json)
        if is_user[1] == 404:
            return is_user
        return OrderController().get_order_history_2(user_id)
    return jsonify(Error='Method not allowed'), 405

@app.route("/office-essentials/Orders/orderhistory", methods=['GET','POST'])
def order_history():
    # had to change method to post because axios ignores bodies within get methods
    if request.method == 'POST':
        print(request.json)
        user_id = request.json['user_id']
        is_user = BaseUser().getUserID(request.json)
        if is_user[1] == 404:
            return is_user
        return OrderController().get_order_history(user_id)
    return jsonify(Error='Method not allowed'), 405

@app.route("/office-essentials/Orders/getallorders")
def get_all_orders():
    if request.method == 'GET':
        return OrderController().get_all_orders()
    return jsonify(Error='Method not allowed'), 405

#####################################################################
#                             Produts                               #
#####################################################################

@app.route("/office-essentials/products/all", methods=['GET', 'POST'])
def handleAllProducts():
    if request.method == 'GET':
        return ProductController().getAllProducts()
    elif request.method == 'POST':
        return ProductController().createProduct(request.json)
    else:
        return jsonify("Method does not exist"), 405


@app.route("/office-essentials/products/id/<int:product_id>", methods=['GET', 'DELETE', 'POST'])
def handleProductByID(product_id):
    if request.method == 'GET':
        return ProductController().getProductID(product_id)
    elif request.method == 'DELETE':
        CartContentsController().delete_from_carts(product_id)
        return ProductController().deleteProduct(product_id, request.json)
    elif request.method == 'POST':
        return ProductController().updateProduct(product_id, request.json)
    else:
        return jsonify("Method does not exist"), 405

@app.route("/office-essentials/products/id/<product_id>/name/<product_name>/price/<int:product_price>/dis/<int:product_dis>/quantity/<int:product_quantity>/category/<product_category>/user/<int:user_id>", methods=['POST'])
def handleProductByUserId(product_id, product_name, product_price, product_dis, product_quantity, product_category, user_id):
    if request.method == 'POST':
        return ProductController().updateProductByUserId(product_id, product_name, product_price, product_dis, product_quantity, product_category, user_id)
    else:
        return jsonify("Method does not exist"), 405

# for frontEnd
@app.route("/office-essentials/products/id/<int:product_id>/user/<int:user_id>", methods=['DELETE'])
def handleProductByIDAndUser(product_id, user_id):
    if request.method == 'DELETE':
        return ProductController().deleteProductUserId(product_id, user_id)
    else:
        return jsonify("Method does not exist"), 405

@app.route("/office-essentials/products/price/id/<int:product_id>", methods=['POST'])
def handleUpdateProductPriceByID(product_id):
    if request.method == 'POST':
        return ProductController().updateProductPrice(product_id, request.json)
    else:
        return jsonify("Method does not exist"), 405

@app.route("/office-essentials/products/quantity/id/<int:product_id>/", methods=['POST'])
def handleUpdateProductQuantityByID(product_id):
    if request.method == 'POST':
        return ProductController().updateProductQuantity(product_id, request.json)
    else:
        return jsonify("Method does not exist"), 405

@app.route("/office-essentials/products/name/<path:order>", methods=['GET'])
def handleProductByName(order):
    if request.method == 'GET':
        return ProductController().getProductNameByOrder(order)
    else:
        return jsonify("Method does not exist"), 405


@app.route("/office-essentials/products/price/<path:order>", methods=['GET'])
def handleProductByPrice(order):
    if request.method == 'GET':
        return ProductController().getProductPriceByOrder(order)
    else:
        return jsonify("Method does not exist"), 405


@app.route("/office-essentials/products/category/<path:category>", methods=['GET'])
def handleProductByCategory(category):
    if request.method == 'GET':
        return ProductController().getProductByCategory(category)
    else:
        return jsonify("Method does not exist"), 405


#####################################################################
#                        Global Statistics                          #
#####################################################################

@app.route("/office-essentials/products/global/most_expensive", methods=['GET'])
def handleProductByMostExpensive():
    if request.method == 'GET':
        return ProductController().getProductMostExpensive()
    else:
        return jsonify("Method does not exist"), 405


@app.route("/office-essentials/products/global/least_expensive", methods=['GET'])
def handleProductByLeastExpensive():
    if request.method == 'GET':
        return ProductController().getProductLeastExpensive()
    else:
        return jsonify("Method does not exist"), 405

@app.route("/office-essentials/products/global/ranking_categories/<int:limit>", methods=['GET'])
def handleProductByGlobalRankingCategories(limit):
    if request.method == 'GET':
        return ProductController().getGlobalRankingCategories(limit)
    else:
        return jsonify("Method does not exist"), 405

@app.route("/office-essentials/products/global/ranking_products/<int:limit>", methods=['GET'])
def handleProductByGlobalRankingProducts(limit):
    if request.method == 'GET':
        return ProductController().getGlobalRankingProducts(limit)
    else:
        return jsonify("Method does not exist"), 405

if __name__ == "main":
    app.run(Debug=1)

