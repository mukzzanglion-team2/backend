from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuoteSerializer
from database import db_connect
from bson.objectid import ObjectId

DB_NAME = 'quote_recommend'
QUOTE_COLLECTION_NAME = 'Quote'

def check(request):  # 잘 돌아가는지 체크용
    return HttpResponse("<h1>Quote service is OK</h1>")

class QuoteList(APIView):
    # [GET] 명언 리스트 조회
    def get(self, request):
        client = db_connect()
        quote_db = client[DB_NAME][QUOTE_COLLECTION_NAME]
        quotes = list(quote_db.find({}, {'_id': 0}))  # 모든 document 검색, _id 제외
        return Response(quotes)
    
    # [POST] 명언 등록
    def post(self, request):
        serializer = QuoteSerializer(data=request.data)  # request에 POST 요청에 들어온 데이터
        if serializer.is_valid():
            serializer.save()  # instance가 없는 경우 serializer의 create를 호출한다
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuoteDetail(APIView):
    def get_object(self, quote_id):
        client = db_connect()
        quote_db = client[DB_NAME][QUOTE_COLLECTION_NAME]
        quote = quote_db.find_one({"_id": ObjectId(quote_id)}, {'_id': 0})
        return quote
    
    # [GET] 해당 ID의 명언 조회
    def get(self, request, quote_id):
        quote = self.get_object(quote_id)
        if quote:
            return Response(quote)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # [PUT] 해당 ID의 명언 정보 수정
    def put(self, request, quote_id):
        quote = self.get_object(quote_id)
        if not quote:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = QuoteSerializer(quote, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # instance가 있는 경우 serializer의 update를 호출한다
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # [DELETE] 해당 ID의 명언 삭제
    def delete(self, request, quote_id):
        client = db_connect()
        quote_db = client[DB_NAME][QUOTE_COLLECTION_NAME]
        result = quote_db.delete_one({"_id": ObjectId(quote_id)})
        if result.deleted_count == 1:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)