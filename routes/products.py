from flask import request, Blueprint, jsonify
from utils.firebase import db
import datetime

product = Blueprint('products', __name__)


@product.route('/product/', methods=['GET', 'POST', 'PUT'])
def Product():
    if request.method == 'GET':
        id = request.args.get('id')
        doc = db.collection(u'products').document('{}'.format(id)).get()
        try:
            if doc.exists == False:
                return jsonify({"data": [], "messsage": "no data"})
            else:
                return jsonify({"data": doc.to_dict()})
        except:
            return jsonify({"data": [], "messsage": "error"})
    elif request.method == 'POST':
        data = request.json
        typeProduct = data['type']
        name = data['name']
        in_stock = data['in_stock']
        description = data['description']
        img = data['img']
        try:
            db.collection(u'products').add({
                u'name': name,
                u'type': typeProduct,
                u'in_stock': int(in_stock),
                u'description': description,
                u'image_url': img,
                u'created_at': datetime.datetime.now()

            })
            return jsonify({u"message": u"Add product sucessfully"})
        except:
            return jsonify({u"message": u"error"})


@product.route('/products/', methods=['GET'])
def Products():
    ref_products = db.collection(u'products')
    typeProduct = request.args.get('type')
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))

    print('[POST] /products/  type:{type} page:{page} limit:{limit}'.format(
        type=typeProduct, page=page, limit=limit))
    try:
        first_query = ref_products.order_by(u'created_at').limit(limit)
        for i in range(page):
            next_query = first_query
            data = next_query.get()
            last_doc = list(data)[-1]
            last_pop = last_doc.to_dict()[u'created_at']
            first_query = ref_products.order_by(u'created_at').start_after({
                u'created_at': last_pop
            }).limit(limit)

        responseData = []
        docs = next_query.get()

        for doc in docs:
            responseData.append(doc.to_dict())

        return jsonify({"data": responseData})
    except:
        return jsonify({"data": []})
