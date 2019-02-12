from flask import Flask, url_for
from utils.firebase import db
from routes.products import product

app = Flask(__name__)

app.register_blueprint(product)

if(__name__ == 'main'):
    app.run(debug=True)
