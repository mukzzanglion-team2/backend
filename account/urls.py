from django.urls import path
from . import views

urlpatterns = [
    path("", views.check, name='check'),                                            # [GET] 잘 돌아가는지 체크용
    path('user/', views.UserList.as_view(), name='user_list'),                     # [GET] 유저 리스트 조회, [POST] 유저 생성
    path('user/<str:email>/', views.UserDetail.as_view(), name='user_detail'),     # [GET] 해당 유저 조회, [PUT] 해당 유저 정보 수정, [DELETE] 해당 유저 삭제
    path('login/', views.UserLogin.as_view()),                                      # [POST] 해당 유저의 로그인 
]