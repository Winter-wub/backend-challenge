from flask import Flask, url_for
from utils.firebase import db
from routes.products import product
from routes.orders import order

app = Flask(__name__)

app.register_blueprint(product)
app.register_blueprint(order)

if(__name__ == 'main'):
    app.run(debug=True)
