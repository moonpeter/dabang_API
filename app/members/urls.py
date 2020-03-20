from django.urls import path

from members import views, apis

urlpatterns_members = [
    path('kakao-login/', views.kakao_login),
    path('django-logout/', views.user_logout),
    path('kakaoToken/', apis.KakaoJwtTokenView.as_view()),
]

