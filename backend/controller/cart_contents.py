from flask import jsonify
from backend.model.cart_contents import CartContentsDAO
from backend.controller.product import ProductController
from backend.controller.cart import CartController

class CartContentsController:

    def build_dict(self, row):
        result = {}
        result['CartId'] = row[0]
        result['ProductId'] = row[1]
        result['ProductQuantity'] = row[2]
        result['ProductName'] = row[3]
        result['ProductPrice'] = round(row[4], 2)
        return result

    def get_all_from_cart(self, cart_id):

        # Check if the cart exists
        is_cart = CartController().get_cart_by_id(cart_id)
        if is_cart[1] == 404:
            return is_cart

        dao = CartContentsDAO()
        product_dao = ProductController
        result_tuples = dao.get_all_from_cart(cart_id)
        result = []
        print(result_tuples)
        if result_tuples:
            for row in result_tuples:
                result.append(self.build_dict(row))
            return result, 200
        return jsonify('Cart is empty'), 404

    def add_to_cart(self, json):

        dao = CartContentsDAO()

        # Check if the cart exists
        cart_id = json['CartId']
        is_cart = CartController().get_cart_by_id(cart_id)
        if is_cart[1] == 404:
            return is_cart

        # Check if the product exists
        product_id = json['ProductId']
        is_product = ProductController().getProductID(product_id)
        if is_product[1] == 404:
            return is_product

        product_quantity = json['ProductQuantity']
        if product_quantity < 0:
            return jsonify('Product quantity cannot be negative.'), 400
        stock_quantity = ProductController().get_product_by_id(product_id)['product_quantity']

        # check if the product is already in the cart
        current_quantity = dao.in_cart(cart_id, product_id)

        if current_quantity:
            new_quantity = current_quantity[0] + product_quantity
            if new_quantity <= stock_quantity:
                result = dao.update_cart(cart_id, product_id, new_quantity)
                return jsonify({'CartId': result[0], 'ProductId': result[1], 'ProductQuantity':result[2]}), 201
            else:
                return jsonify('Cannot add more than what is in stock'), 400

        else:
            if product_quantity <= stock_quantity:
                result = dao.add_to_cart(cart_id, product_id, product_quantity)
                return jsonify({'CartId': result[0], 'ProductId': result[1], 'ProductQuantity': result[2]}), 201
            return jsonify('Cannot add more than what is in stock'), 400

    def remove_from_cart(self, json):

        # Check if the cart exists
        cart_id = json['CartId']
        is_cart = CartController().get_cart_by_id(cart_id)
        if is_cart[1] == 404:
            return is_cart

        dao = CartContentsDAO()
        product_id = json['ProductId']
        product_quantity = json['ProductQuantity']
        if product_quantity < 0:
            return jsonify('Product quantity cannot be negative.'), 400

        result_tuple = dao.in_cart(cart_id, product_id)

        if result_tuple:
            current_quantity = result_tuple[0]

            # Update the quantity if we remove less than what is in the cart
            if current_quantity - product_quantity > 0:
                new_quantity = current_quantity - product_quantity
                dao.update_cart(cart_id, product_id, new_quantity)
                return self.get_all_from_cart(18)

            # Remove the item if the quantity equals what is in the cart
            elif current_quantity - product_quantity == 0:
                dao.remove_from_cart(cart_id, product_id)
                print('----------------Hi--------------------------')
                print(self.get_all_from_cart(18))
                return self.get_all_from_cart(18)

            # throw a warning if what is to be removed exceeds what is in the cart
            else:
                return jsonify('You cannot remove from the cart more than what you have.'), 400
        return jsonify('The item you specified is not in the cart'), 404

    def remove_all(self, cart_id):

        # Check if the cart exists
        is_cart = CartController().get_cart_by_id(cart_id)
        if is_cart[1] == 404:
            return is_cart

        dao = CartContentsDAO()
        result_tuples = dao.get_all_from_cart(cart_id)
        # Clears the cart
        if result_tuples:
            result = []
            for row in result_tuples:
                result.append((self.build_dict(row)))
            dao.clear_cart(cart_id)
            return jsonify(result), 200

        # Takes care if the cart is empty
        else:
            return jsonify('Cart is empty'), 400

    def delete_from_carts(self, product_id):
        dao = CartContentsDAO()
        result = dao.delete_from_carts(product_id)
        if result:
            return jsonify(result), 200
        return jsonify('Product not found'), 404

    def calculate_subtotal(self, cart_id):
        dao = CartContentsDAO()
        result = dao.calculate_subtotal(cart_id)
        return jsonify(result)

    def delete_all_from_cart(self, cart_id, product_id):
        dao = CartContentsDAO()
        dao.delete_all_from_cart(cart_id, product_id)
        return jsonify({'CartID':cart_id, 'ProductID':product_id})
