import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate(
    'C:/Users/wave_/developer-challange-1bf4eca39862.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
