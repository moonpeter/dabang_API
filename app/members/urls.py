from django.urls import path, include
from rest_framework.routers import DefaultRouter

from members import apis, views
from members.apis import KakaoSignInCallbackView, socialLogin

router = DefaultRouter()
router.register('viewset', views.UserViewSet)

urlpatterns_members = [
    path('kakao-login/', views.kakao_login),
    path('django-logout/', views.user_logout),
    path('kakaoToken/', apis.KakaoJwtTokenView.as_view()),
    path('facebookToken/', apis.FacebookJwtToken.as_view()),
    path('kakaoTest/', apis.KAKAO.as_view()),
    path('sign-in/kakao/callback/', KakaoSignInCallbackView.as_view()),

    path('kakao-login/', views.kakao_login),
    path('socialLogin/', socialLogin.as_view()),


]
