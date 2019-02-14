import firebase_admin
from firebase_admin import credentials, firestore
import os
# Use a service account
cred = credentials.Certificate(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
firebase_admin.initialize_app(cred)


db = firestore.client()
