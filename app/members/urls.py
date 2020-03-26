from django.urls import path, include
from rest_framework.routers import DefaultRouter

from members import views, apis

router = DefaultRouter()
router.register('viewset', views.UserViewSet)

urlpatterns_members = [
    # path('changePassword/', apis.changePassword.as_view()),
    path('get-token/', apis.UserJwtToken.as_view()),
    path('kakao-login/', views.kakao_login),
    path('facebook-login/', views.facebook_login),
    path('django-logout/', views.user_logout),
    path('kakaoToken/', apis.KakaoJwtTokenView.as_view()),
    path('facebookToken/', apis.FacebookJwtToken.as_view()),
    path('', include(router.urls)),
    path('SignUpView/', apis.SignUpView.as_view()),
    # path('authToken/', apis.AuthToken.as_view()),
]
