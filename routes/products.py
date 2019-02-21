from flask import request, Blueprint, jsonify
from flask_cors import CORS
from utils.firebase import db
from managers.products import getProductbyId, addProduct
import datetime

product = Blueprint('products', __name__)
CORS(product)


@product.route('/product/', methods=['GET', 'POST', 'PUT'])
def Product():
    if request.method == 'GET':
        id = request.args.get('id')
        doc = getProductbyId(id)
        if doc is None:
            return jsonify({"data": [], "messsage": "no data"})
        else:
            return jsonify({"data": doc})
    elif request.method == 'POST':
        data = request.json
        typeProduct = data['type']
        name = data['name']
        in_stock = data['in_stock']
        description = data['description']
        img = data['img']
        if addProduct(typeProduct, name, int(in_stock), img, description) is True:
            return jsonify({u"message": u"Add product sucessfully"})
        else:
            return 500
    elif request.method == 'PUT':
        reqBody = request.json
        id = request.args.get('id')

        try:
            querySnapshot = db.collection(
                u'products').document('{}'.format(id)).get()
            if querySnapshot.exists == False:
                return jsonify({u"message": "no document that contain id {}".format(id)})
            else:
                doc = querySnapshot.to_dict()
                typeProduct = reqBody.get('type') or doc['type']
                name = reqBody.get('name') or doc['name']
                in_stock = reqBody.get('in_stock') or doc['in_stock']
                description = reqBody.get('description') or doc['description']
                img = reqBody.get('img') or doc['image_url']

                updateData = {
                    u'name': name,
                    u'type': typeProduct,
                    u'in_stock': int(in_stock),
                    u'description': description,
                    u'image_url': img,
                    u'updated_at': datetime.datetime.now(),
                    u'created_at': doc['created_at']
                }

                db.collection(u'products').document(id).set(updateData)
                return jsonify({u'messsage': 'update product id {} is sucessfully'.format(id)})
        except Exception as e:
            return jsonify({u"error": '{}'.format(e)})


@product.route('/products/', methods=['GET'])
def Products():
    ref_products = db.collection(u'products')
    typeProduct = request.args.get('type')
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    try:
        if typeProduct == 'all':
            first_query = ref_products.order_by(u'created_at').limit(limit)
            for i in range(page):
                next_query = first_query
                data = next_query.get()
                last_doc = list(data)[-1]
                last_pop = last_doc.to_dict()[u'created_at']
                first_query = ref_products.order_by(u'created_at').start_after({
                    u'created_at': last_pop
                }).limit(limit)
        else:
            first_query = ref_products.where(
                'type', '==', typeProduct).order_by(u'created_at').limit(limit)
            for i in range(page):
                next_query = first_query
                data = next_query.get()
                last_doc = list(data)[-1]
                last_pop = last_doc.to_dict()[u'created_at']
                first_query = ref_products.where(
                    'type', '==', typeProduct).order_by(u'created_at').start_after({
                        u'created_at': last_pop
                    }).limit(limit)

        responseData = []
        docs = next_query.get()

        for doc in docs:
            responseData.append({u"id": doc.id, **doc.to_dict()})

        return jsonify({"data": responseData})
    except:
        return jsonify({"data": []})
