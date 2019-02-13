from utils.firebase import db


def getProductbyId(id):
    try:
        doc = db.collection(u'products').document(id).get()
        if doc.exists is True:
            return doc.to_dict()
        else:
            return None
    except Exception as e:
        print(e)
        return None
