from flask import jsonify
from datetime import date
from backend.model.order import OrderDAO
import copy

class OrderController:

    def build_dict(self, row):
        result = {}
        result['order_id'] = row[0]
        result['order_subtotal'] = row[1]
        result['order_tax'] = row[2]
        result['order_total'] = row[3]
        result['order_date'] = row[4]
        return result

    def build_order_history(self, row, info):
        info['Items'].append({'ProductName': row[1], 'ProductPrice': row[2], 'ProductQuantity': row[3]})
        return info

    def new_order(self, order_subtotal, user_id):
        dao = OrderDAO()
        order_tax = round((order_subtotal * 0.115), 2)
        order_total = round(order_subtotal + order_tax, 2)
        order_date = date.today().strftime("%B %d, %Y")
        result = dao.new_order(order_subtotal, order_tax, order_total, order_date, user_id)
        return result

    def delete_order(self, order_id):
        dao = OrderDAO()
        result = dao.delete_order(order_id)
        return jsonify(result), 200

    def get_order_by_id(self, order_id):
        dao = OrderDAO()
        result_tuples = dao.get_order_by_id(order_id)
        result = []
        if result_tuples:
            for row in result_tuples:
                result.append(self.build_dict(row))
            return result, 200
        return jsonify('Not Found'), 404

    def get_all_orders(self):
        dao = OrderDAO()
        result_tuples = dao.get_all_orders()
        result = []
        if result_tuples:
            for row in result_tuples:
                result.append(self.build_dict(row))
        return jsonify(result) , 200

    def get_order_total(self, order_id):
        dao = OrderDAO()
        result = dao.get_order_total(order_id)
        return result

    def get_order_history_2(self, user_id):
        dao = OrderDAO()
        result_tuples = dao.get_order_history_2(user_id)
        result = []
        if result_tuples:
            first_order_id = result_tuples[0][0]
            info = {'OrderID': first_order_id, 'Items':[]}
            previous_tuple = None
            for i, row in enumerate(result_tuples):
                if previous_tuple:
                    if previous_tuple[0] != row[0]:
                        print(row)
                        info['OrderSubtotal'] = previous_tuple[4]
                        info['OrderTax'] = previous_tuple[5]
                        info['OrderTotal'] = previous_tuple[6]
                        info['OrderDate'] = previous_tuple[7]
                        result.append(copy.deepcopy(info))
                        info.clear()
                        info['OrderID'] = row[0]
                        info['Items'] = []
                        self.build_order_history(row, info)
                        if i == len(result_tuples) - 1:
                            info['OrderSubtotal'] = previous_tuple[4]
                            info['OrderTax'] = previous_tuple[5]
                            info['OrderTotal'] = previous_tuple[6]
                            info['OrderDate'] = previous_tuple[7]
                            result.append(info)
                    else:
                        self.build_order_history(row, info)
                        if i == len(result_tuples) - 1:
                            info['OrderSubtotal'] = row[4]
                            info['OrderTax'] = row[5]
                            info['OrderTotal'] = row[6]
                            info['OrderDate'] = row[7]
                            result.append(info)
                else:
                    self.build_order_history(row, info)
                    if len(result_tuples) == 1:
                        info['OrderSubtotal'] = row[4]
                        info['OrderTax'] = row[5]
                        info['OrderTotal'] = row[6]
                        info['OrderDate'] = row[7]
                        result.append(info)
                previous_tuple = row
            return jsonify(result), 200
        else:
            return jsonify('You have no orders at the moment.'), 404

    def get_user_orders(self, user_id):
        dao = OrderDAO()
        result_tuples = dao.get_user_orders(user_id)
        if result_tuples:
            return result_tuples, 200
        return jsonify('User has no orders.'), 404

    def delete_by_user_id(self, user_id):
        dao = OrderDAO()
        result_tuples = dao.delete_by_user_id(user_id)
        if result_tuples:
            return result_tuples, 200
        return jsonify('User has no orders.'), 404

    def get_order_history(self, user_id):
        dao = OrderDAO()
        result_tuples = dao.get_order_history(user_id)
        result = []
        if result_tuples:
            for row in result_tuples:
                result.append(self.build_dict(row))
            return jsonify(result), 200
        else:
            return jsonify('User has no orders.'), 404