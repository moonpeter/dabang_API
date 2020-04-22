from django.urls import path, include
from rest_framework.routers import DefaultRouter

from members import apis
from members.apis import socialLogin

router = DefaultRouter()
router.register('viewset', apis.UserModelViewSet)

urlpatterns_members = [
    path('socialLogin/', socialLogin.as_view()),

]
