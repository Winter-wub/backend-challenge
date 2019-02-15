from flask import Flask
from flask_cors import CORS
from utils.firebase import db
from routes.products import product
from routes.orders import order
from routes.customers import customers

app = Flask(__name__)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


app.register_blueprint(product)
app.register_blueprint(order)
app.register_blueprint(customers)

app.run(host='0.0.0.0', port=5000)
