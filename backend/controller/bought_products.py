from flask import jsonify
from backend.model.bought_products import BoughtProductsDAO


class BoughtProductsController:

    def add_to_order_his(self, order_id, product_id, product_price, product_quantity, product_name):
        dao = BoughtProductsDAO()
        result = dao.add_to_order_his(order_id, product_id, product_price, product_quantity, product_name)
        return result

    def delete_order(self, order_id):
        dao = BoughtProductsDAO()
        result_order_id = dao.delete_order(order_id)
        if result_order_id:
            return jsonify(result_order_id), 200
        else:
            return jsonify('Not Found'), 404

    def receipt(self, order_id, order_subtotal, order_tax, order_total, order_date):
        dao = BoughtProductsDAO()
        result_tuples = dao.get_all(order_id)
        result = []
        order = {'OrderID': order_id, 'Items': []}
        for row in result_tuples:
            product_price = row[2]
            product_quantity = row[3]
            product_name = row[4]
            order['Items'].append({'ProductName': product_name, 'ProductQuantity': product_quantity, 'ProductPrice': product_price})
        order['OrderSubtotal'] = order_subtotal
        order['OrderTax'] = order_tax
        order['OderTotal'] = order_total
        order['OrderDate'] = order_date
        result.append(order)
        return result
