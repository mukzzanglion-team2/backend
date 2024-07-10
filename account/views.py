from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UserLoginSerializer
from database import db_connect

DB_NAME = 'quote_recommend'
COLLECTION_NAME = 'User'

def check(request):  # 잘 돌아가는지 체크용
    return HttpResponse("<h1>Account is OK</h1>")

class UserList(APIView):
    # [GET] 유저 리스트 조회
    def get(self, request):
        client = db_connect()
        user_db = client[DB_NAME][COLLECTION_NAME]
        users = list(user_db.find({}, {'_id': 0}))  # 모든 document 검색, _id 제외
        return Response(users)
    
    # [POST] 유저 생성
    def post(self, request):
        serializer = UserSerializer(data=request.data)  # request에 POST 요청에 들어온 데이터
        if serializer.is_valid():
            serializer.save()  # instance가 없는 경우 serializer의 create를 호출한다
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    def get_object(self, email):
        client = db_connect()
        user_db = client[DB_NAME][COLLECTION_NAME]
        user = user_db.find_one({"email": email}, {'_id': 0})
        return user
    
    # [GET] 해당 Email의 유저 조회
    def get(self, request, email):
        user = self.get_object(email)
        if user:
            return Response(user)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # [PUT] 해당 Email의 유저 정보 수정
    def put(self, request, email):
        user = self.get_object(email)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # instance가 있는 경우 serializer의 update를 호출한다
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # [DELETE] 해당 Email의 유저 삭제
    def delete(self, request, email):
        client = db_connect()
        user_db = client[DB_NAME][COLLECTION_NAME]
        result = user_db.delete_one({"email": email})
        if result.deleted_count == 1:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class UserLogin(APIView):
    # [POST] 유저 로그인 시도
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "로그인 성공"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)