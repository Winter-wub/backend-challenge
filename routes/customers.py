from flask import request, Blueprint, jsonify
from flask_cors import CORS
from utils.firebase import db
import bcrypt
import datetime

customers = Blueprint('customers', __name__)
CORS(customers)


@customers.route('/customers/', methods=['GET'])
def getcustomers():
    if request.method == 'GET':
        role = request.args.get('role') or 'normal'
        try:
            querySnapshot = db.collection(u'customers').where(
                u'role', '==', role).get()
            customers = []
            for doc in querySnapshot:
                userData = doc.to_dict()
                customers.append({u'id': doc.id, u'username': userData['username'],
                                  u'name': userData['name'], u'role': userData['role'], u'address': userData['address']})

            return jsonify({u"data": customers})
        except Exception as e:
            return jsonify({u'error': e})
    else:
        return 405


@customers.route('/customer/', methods=['POST', 'PUT'])
def customer():
    if request.method == 'POST':
        try:
            name = request.json['name']
            address = request.json.get('address') or ''
            username = request.json['username']
            password = bcrypt.hashpw(
                request.json['password'].encode('utf-8'), bcrypt.gensalt())

            db.collection(u'customers').add({
                u'username': username,
                u'password': password,
                u'address': address,
                u'role': u'normal',
                u'created_at':  datetime.datetime.now(),
                u'name': name
            })

            return jsonify({u'message': 'Add user successfully'})

        except Exception as e:
            return jsonify({u'error': e})
    elif request.method == 'PUT':
        try:
            userId = request.json['id']

            currentUserData = db.collection(
                u'customers').document(userId).get()

            if currentUserData.exists is False:
                return 400

            currentUserData = currentUserData.to_dict()
            address = request.json.get('address') or currentUserData['address']
            name = request.json.get('name') or currentUserData['name']

            updateData = {
                **currentUserData,
                u'updated_at': datetime.datetime.now(),
                u'name': name,
                u'address': address,
            }

            if request.json.get('password'):
                password = bcrypt.hashpw(
                    request.json['password'].encode('utf-8'), bcrypt.gensalt())
                updateData = {
                    **updateData,
                    u'password': password
                }
            db.collection(u'customers').document(userId).set(updateData)

            return jsonify({u'message': 'user id: {} is update sucessfully'.format(userId)})
        except Exception as e:
            return jsonify({u'error': e})
    else:
        return 405


@customers.route('/login/', methods=['POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password'].encode('utf-8')

        querySnapshot = db.collection(u'customers').where(
            'username', '==', username).get()
        userData = []
        for doc in querySnapshot:
            userData.append({u'id': doc.id, **doc.to_dict()})

        if len(userData) == 0:
            return jsonify({u'message': u'No user in database'}), 400

        currentUserData = userData[0]
        if bcrypt.checkpw(password, currentUserData['password']) is True:
            return jsonify({
                u'data': {
                    u'username': currentUserData['username'],
                    u'name': currentUserData['name'],
                    u'role': currentUserData['role'],
                    u'address': currentUserData['address']
                }
            })
        else:
            return jsonify({u'message': u'Password incorrect'}), 400
    except Exception as e:
        return jsonify({u'error': e}), 500
