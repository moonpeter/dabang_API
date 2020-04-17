from django.urls import path, include
from rest_framework.routers import DefaultRouter

from members import apis, views
from members.apis import KakaoSignInCallbackView, testSoical

router = DefaultRouter()
router.register(r'user', apis.UserModelViewSet, basename='UserModel')

urlpatterns_members = [
    path('kakaoToken/', apis.KakaoJwtTokenView.as_view()),
        path('facebookToken/', apis.FacebookJwtToken.as_view()),

    path('kakaoTest/', apis.KAKAO.as_view()),
    path('sign-in/kakao/callback/', KakaoSignInCallbackView.as_view()),

    path('kakao-login/', views.kakao_login),
    path('test/', testSoical.as_view()),

]
urlpatterns_members += router.urls
