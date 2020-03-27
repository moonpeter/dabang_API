from django.urls import path, include
from rest_framework.routers import DefaultRouter

from members import views, apis

router = DefaultRouter()
router.register('user', views.UserViewSet)

urlpatterns_members = [
    path('', include(router.urls)),
    path('SignUpView/', apis.SignUpView.as_view()),
    path('get-token/', apis.UserJwtToken.as_view()),
    path('kakaoToken/', apis.KakaoJwtTokenView.as_view()),
    path('facebookToken/', apis.FacebookJwtToken.as_view()),
]
