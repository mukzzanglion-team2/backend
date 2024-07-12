from rest_framework import serializers
from database.database import db_connect

DB_NAME = "quote_recommend"
COLLECTION_NAME = "User"

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_blank=False, max_length=50)                                        # Not NULL
    password = serializers.CharField(allow_blank=False, max_length=30, write_only=True)                     # Not NULL
    nickname = serializers.CharField(allow_blank=False, min_length=1, max_length=20)                        # Not NULL      
    name = serializers.CharField(allow_blank=False, max_length=50)                                          # Not NULL
    age = serializers.IntegerField(min_value=1, max_value=100)                                              # Not NULL
    sex = serializers.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')])                         # Not NULL
    birth = serializers.RegexField(regex=r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$', min_length=10, max_length=10)     # Not NULL
    phone = serializers.RegexField(regex=r'^010-[0-9]{3,4}-[0-9]{4}$', min_length=12, max_length=13)        # Not NULL

    followers = serializers.ListField(required=False, child=serializers.CharField())            # User의 _id(objectId)의 str 변환값들의 리스트
    following = serializers.ListField(required=False, child=serializers.CharField())            # User의 _id(objectId)의 str 변환값들의 리스트
    registered_quotes = serializers.ListField(required=False, child=serializers.CharField())    # Quote의 _id(objectId)의 str 변환값들의 리스트
    liked_quotes = serializers.ListField(required=False, child=serializers.CharField())         # Quote의 _id(objectId)의 str 변환값들의 리스트

    def create(self, data):
        client = db_connect()
        user_db = client[DB_NAME][COLLECTION_NAME]
        data['followers'] = []
        data['following'] = []
        data['registered_quotes'] = []
        data['liked_quotes'] = []
        user_db.insert_one(data)
        return data

    def update(self, existing_user, data):
        client = db_connect()
        user_db = client[DB_NAME][COLLECTION_NAME]
        user_db.update_one({'email' : existing_user['email']}, {'$set' : data}) # email로 찾고 data로 update
        return data
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50, allow_blank=False)
    password = serializers.CharField(max_length=30, allow_blank=False)
    
    def validate(self, data):
        client = db_connect()
        user_db = client[DB_NAME][COLLECTION_NAME]
        user = user_db.find_one({"email": data['email']}) # Email로 해당 User를 찾고
        if (not user) or (user['password'] != data['password']): # 만약 없는 User거나 비밀번호가 틀렸으면
            raise serializers.ValidationError("아이디(로그인 전용 아이디) 또는 비밀번호가 잘못 되었습니다. 아이디와 비밀번호를 정확히 입력해 주세요.")
        return data