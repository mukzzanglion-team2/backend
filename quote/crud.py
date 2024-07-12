from database.database import db_connect
from bson.objectid import ObjectId

DB_NAME = 'quote_recommend'
COLLECTION_NAME = 'Quote'

def find_quote(quote_id):
    client = db_connect()
    quote_db = client[DB_NAME][COLLECTION_NAME]
    try:
        quote = quote_db.find_one({'_id' : ObjectId(quote_id)})
        quote['_id'] = quote_id
        return quote
    except Exception as e:
        print(f"Error : {e}")
        return None