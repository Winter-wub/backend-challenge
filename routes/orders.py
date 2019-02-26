from flask import request, Blueprint, jsonify
from flask_cors import CORS
from utils.firebase import db
import datetime
import omise

omise.api_secret = 'skey_test_5f1ww1anxcomivbbwql'
omise.api_public = 'pkey_test_5f1ww1annj0f10en08t'

order = Blueprint('orders', __name__)
CORS(order)


def checkProductExist(productIds):
    productFailtoCreateOrder = []
    productSuccesstoCreateOrder = []
    for product in productIds:
        querySnapshot = db.collection(
            u'products').document(product['id']).get()
        if querySnapshot.exists is True:
            productDataRef = querySnapshot
            productData = productDataRef.to_dict()
            productId = productDataRef.id
            if int(productData['in_stock']) < int(product['value']):
                productFailtoCreateOrder.append({**product, u'id': productId})
            else:
                productSuccesstoCreateOrder.append(
                    {**product, u'id': productId})
        else:
            productFailtoCreateOrder.append(product)
    return productSuccesstoCreateOrder, productFailtoCreateOrder


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
            productSuccesstoCreateOrder, productFailtoCreateOrder = checkProductExist(
                productIds)
            docRef = db.collection(u'orders').add({
                u'user_id': userId,
                u'product_ids': productSuccesstoCreateOrder,
                u'created_at':  datetime.datetime.now(),
                u'status': 'waiting'
            })
            return jsonify({u'data': {
                u'id': docRef[1].id,
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


@order.route('/payment', methods=['POST'])
def payment():
    if request.method == 'POST':
        data = request.json['data']
        cardInfo = data['card_info']
        orderInfo = data['order']
        orderId = orderInfo['orderId']
        orderRef = db.collection('orders').document(orderId)
        productIds = orderRef.get().to_dict()['product_ids']
        avalibleProduct, notAvaliableProduct = checkProductExist(productIds)
        if len(notAvaliableProduct) > 0:
            return jsonify({u'message': 'some product is not avaliable please try again'})
        else:
            totalprice = 0
            for product in productIds:
                productRef = db.collection('products').document(product['id'])
                productData = productRef.get().to_dict()
                updateProduct = {
                    **productData,
                    'in_stock': int(productData['in_stock']) - int(product['value'])
                }
                productRef.set(updateProduct)

                totalprice = int(product['price']) * \
                    int(product['value']) + totalprice
            charges = omise.Charge.create(
                description=orderId,
                amount=totalprice*10,
                currency='thb',
                card=cardInfo['id']
            )
            if (charges.paid):
                currentOrder = orderRef.get().to_dict()
                newOrder = {
                    **currentOrder,
                    u'status': 'paid'
                }
                orderRef.set(newOrder)
            return 'ok'

    else:
        return 405
