from database.database import db_connect
from bson.objectid import ObjectId

DB_NAME = 'quote_recommend'
COLLECTION_NAME = 'User'

def find_user(user_id):
    client = db_connect()
    user_db = client[DB_NAME][COLLECTION_NAME]
    try:
        user = user_db.find_one({'_id' : ObjectId(user_id)})
        user['_id'] = user_id
        return user
    except Exception as e:
        print(f"Error : {e}")
        return None

def update_registered_quotes(user_id, quote_id, func):
    client = db_connect()
    user_db = client[DB_NAME][COLLECTION_NAME]
    try:
        if func == 'push':
            user_db.update_one(
                {'_id' : ObjectId(user_id)},
                {'$push': {'registered_quotes': quote_id}})
        else:
            user_db.update_one(
                {'_id' : ObjectId(user_id)},
                {'$pull': {'registered_quotes': quote_id}})
    except Exception as e:
        print(f"Error : {e}")