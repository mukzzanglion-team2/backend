from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuoteSerializer
from database.database import db_connect, vector_connect
from account.crud import find_user, update_registered_quotes
from bson.objectid import ObjectId

DB_NAME = 'quote_recommend'
COLLECTION_NAME = 'Quote'

def check(request):  # 잘 돌아가는지 체크용
    return HttpResponse("<h1>Quote service is OK</h1>")

class QuoteList(APIView):
    # [GET] 명언 리스트 조회
    def get(self, request):
        client = db_connect()
        quote_db = client[DB_NAME][COLLECTION_NAME]
        quotes = list(quote_db.find({}, {'_id': 0}))  # 모든 document 검색, _id 제외
        return Response(quotes)
    
    # [POST] 명언 등록 --> ChromaDB 연동 완료 --> User의 registered_quotes에 quote_id 추가
    def post(self, request):
        serializer = QuoteSerializer(data=request.data)  # request에 POST 요청에 들어온 데이터
        if serializer.is_valid():
            # serializer.save()  # instance가 없는 경우 serializer의 create를 호출한다
            client = db_connect()
            quote_db = client[DB_NAME][COLLECTION_NAME]
            user_id = serializer.data['registrant']
            user = find_user(user_id)
            if not user:
                return Response(status=status.HTTP_404_NOT_FOUND)

            # MongoDB에 저장
            result = quote_db.insert_one(serializer.data)
            quote_id = str(result.inserted_id) # ObjectId를 문자열로 반환

            # User의 registered_quotes에 quote_id 추가
            update_registered_quotes(user_id, quote_id, 'push')
            
            # ChromaDB에 저장
            manager = vector_connect()
            manager.add_quote(
                description=serializer.data['description'],
                quote_id=quote_id,
                quote=serializer.data['content'],
                author=serializer.data['author'],
            )

            response_data = serializer.data
            response_data['id'] = quote_id
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuoteDetail(APIView):
    def get_object(self, quote_id):
        client = db_connect()
        quote_db = client[DB_NAME][COLLECTION_NAME]
        quote = quote_db.find_one({"_id": ObjectId(quote_id)}, {'_id': 0})
        return quote
    
    # [GET] 해당 ID의 명언 조회
    def get(self, request, quote_id):
        quote = self.get_object(quote_id)
        # manager = vector_connect()
        # doc = manager.get_quote_by_quote_id(quote_id)
        # print(doc)
        if quote:
            return Response(quote)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # [PUT] 해당 ID의 명언 정보 수정 --> ChromaDB 연동 완료
    def put(self, request, quote_id):
        client = db_connect()
        quote_db = client[DB_NAME][COLLECTION_NAME]
        quote = quote_db.find_one({"_id": ObjectId(quote_id)}, {'_id': 0})
        if not quote:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
        data_dict = {key: value for key, value in request.data.items()}
        try:
            # MongoDB Update
            quote_db.update_one({'_id': ObjectId(quote_id)}, {'$set': data_dict})
            # ChromaDB Update
            changed_quote = quote_db.find_one({"_id": ObjectId(quote_id)}, {'_id': 0}) # 수정된 quote을 찾아오고
            
            manager = vector_connect()
            manager.delete_quote_by_quote_id(quote_id) # 기존 Quote은 Chroma에서 없애고
            manager.add_quote(
                description=changed_quote['description'],
                quote_id=quote_id,                      # 기존 quote_id로 저장
                quote=changed_quote['content'],
                author=changed_quote['author'],
            )
            return Response(data_dict, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"error" : "bad"}, status=status.HTTP_400_BAD_REQUEST)
    
    # [DELETE] 해당 ID의 명언 삭제 --> ChromaDB 연동 완료 --> User의 registered_quotes에 quote_id 삭제
    def delete(self, request, quote_id):
        client = db_connect()
        quote_db = client[DB_NAME][COLLECTION_NAME]
        quote = quote_db.find_one({"_id": ObjectId(quote_id)}, {'_id': 0})
        user_id = quote['registrant']

        # MongoDB에서 삭제
        result = quote_db.delete_one({"_id": ObjectId(quote_id)})

        # User의 regeistered_quotes에서 해당 quote_id 삭제
        update_registered_quotes(user_id, quote_id, 'pull')

        # ChromaDB에서 삭제
        manager = vector_connect()
        manager.delete_quote_by_quote_id(quote_id)
        if result.deleted_count == 1:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
def recommend_quote(request):
    if request.method == 'POST':
        try:
            query = request.POST.get('query')
            if not query:
                return JsonResponse({'error': 'Query parameter is required'}, status=400)
            manager = vector_connect()
            retrieved_quote = manager.search_quote(query=query)[0] # 1개만 있는 List이므로
            data = {
                'author' : retrieved_quote.metadata.get('author'),
                'quote' : retrieved_quote.metadata.get('quote'),
                'description' : retrieved_quote.page_content,
            }
            return JsonResponse(data=data, status=200, safe=False) # 비사전 객체도 반환(safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)