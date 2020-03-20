from django.urls import path, include
from rest_framework.routers import DefaultRouter

from members import views, apis

router = DefaultRouter()
router.register('viewset', views.UserViewSet)

urlpatterns_members = [
    path('kakao-login/', views.kakao_login),
    path('django-logout/', views.user_logout),
    path('kakaoToken/', apis.KakaoJwtTokenView.as_view()),
    path('', include(router.urls)),
    path('authToken/', apis.AuthToken.as_view()),
]
