from flask import request, Blueprint, jsonify
from utils.firebase import db
import datetime

order = Blueprint('orders', __name__)


@order.route('/orders/', methods=['GET'])
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


@order.route('/order/', methods=['POST', 'PUT'])
def add_order():
    if request.method == 'POST':
        try:
            userId = request.json['user_id']
            productId = request.json['product_id']
            value = request.json.get('value') or 1

            db.collection(u'orders').add({
                u'user_id': userId,
                u'product_id': productId,
                u'value': value,
                u'created_at':  datetime.datetime.now(),
                u'status': 'waiting'
            })

            return jsonify({u'message': 'add order sucessfully'})

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
