from rest_framework import serializers
from database.database import db_connect
from datetime import datetime

DB_NAME = "quote_recommend"
COLLECTION_NAME = "Quote"

class QuoteSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    author = serializers.CharField(max_length=100)      # 해당 명언의 원발화자
    registrant = serializers.CharField(max_length=100)  # 작성자(User)의 ObjectID
    tag = serializers.ListField(child=serializers.CharField())
    
    image = serializers.ImageField(required=False, allow_null=True)
    likes = serializers.IntegerField(required=False, default=0)
    comments = serializers.ListField(required=False, child=serializers.CharField())
    created_at = serializers.DateTimeField(required=False, default=datetime.now())

    def create(self, data):
        client = db_connect()
        quote_db = client[DB_NAME][COLLECTION_NAME]
        data['likes'] = 0
        data['comments'] = []
        data['created_at'] = datetime.now()
        result = quote_db.insert_one(data)
        data['_id'] = str(result.inserted_id)
        return data

    # def update(self, instance, data):
    #     client = db_connect()
    #     quote_db = client[DB_NAME][COLLECTION_NAME]
    #     quote_db.update_one({'_id': instance['_id']}, {'$set': data})
    #     return data