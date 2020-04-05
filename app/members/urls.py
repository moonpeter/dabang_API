from django.urls import path, include
from rest_framework.routers import DefaultRouter

from members import views, apis

router = DefaultRouter()
router.register(r'user', views.UserModelViewSet, basename='UserModel')

urlpatterns_members = [
    path('kakaoToken/', apis.KakaoJwtTokenView.as_view()),
    path('facebookToken/', apis.FacebookJwtToken.as_view()),
]
urlpatterns_members += router.urls
