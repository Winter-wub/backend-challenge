from flask import request, Blueprint, jsonify
from flask_cors import CORS
from utils.firebase import db
import datetime

order = Blueprint('orders', __name__)
CORS(order)


@order.route('/orders', methods=['GET'])
def orders():
    if request.method == 'GET':
        userId = request.args.get('id')
        try:
            querySnapshot = db.collection(u'orders').where(
                u'user_id', '==', userId).get()
            userOrder = []
            for doc in querySnapshot:
                userOrder.append({u'id': doc.id, **doc.to_dict()})

            return jsonify({u"data": userOrder})
        except Exception as e:
            return jsonify({u'error': e})
    else:
        return 405


@order.route('/order', methods=['POST', 'PUT'])
def add_order():
    if request.method == 'POST':
        try:
            userId = request.json['user_id']
            productIds = request.json['product_ids']
            value = request.json.get('value') or 1
            productFailtoCreateOrder = []
            productSuccesstoCreateOrder = []
            for product in productIds:
                querySnapshot = db.collection(
                    u'products').document(product['id']).get()

                if querySnapshot.exists is True:
                    productData = querySnapshot.to_dict()
                    if productData['in_stock'] < product['value']:
                        productFailtoCreateOrder.append(product)
                    else:
                        productSuccesstoCreateOrder.append(product)
                        db.collection(u'orders').add({
                            u'user_id': userId,
                            u'product_ids': productIds,
                            u'value': value,
                            u'created_at':  datetime.datetime.now(),
                            u'status': 'waiting'
                        })
                else:
                    productFailtoCreateOrder.append(product)

            return jsonify({u'data': {
                u'failed': productFailtoCreateOrder,
                u'success': productSuccesstoCreateOrder
            }})

        except Exception as e:
            return jsonify({u'error': e})
    elif request.method == 'PUT':
        try:
            orderId = request.json['order_id']
            status = request.json['status']

            currentOrder = db.collection(u'orders').document(orderId).get()
            if currentOrder.exists == False:
                return jsonify({u'message': u'order id is not exists'}), 400
            currentOrderData = currentOrder.to_dict()
            updateOrder = {
                **currentOrderData,
                u'updated_at': datetime.datetime.now(),
                u'status': status,
                u'value': request.json.get('value') or currentOrderData['value']
            }

            db.collection(u'orders').document(orderId).set(updateOrder)

            return jsonify({u'message': 'order id: {} is update sucessfully'.format(orderId)})
        except Exception as e:
            return jsonify({u'error': e})
    else:
        return 405
