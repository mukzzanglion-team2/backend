from django.urls import path
from . import views

urlpatterns = [
    path("", views.check, name='check'),                                                # [GET] 잘 돌아가는지 체크용
    path('quotes/', views.QuoteList.as_view(), name='quote_list'),                      # [GET] 명언 리스트 조회, [POST] 명언 등록(Chroma연동)
    path('quotes/<str:quote_id>/', views.QuoteDetail.as_view(), name='quote_detail'),   # [GET] 해당 ID의 명언 조회, [PUT] 해당 ID의 명언 수정(Chroma연동), [DELETE] 해당 ID의 명언 삭제(Chroma연동)
    path('recommend/', views.recommend_quote, name='recommend_quote'),                  # [POST] query에 대해 유사한 맥락의 명언 반환
]