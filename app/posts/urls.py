from django.urls import path

from posts import apis
from posts.apis import getBorodCityList, getEupMyunDongList, getSiGunGuList
from posts.views import test

urlpatterns_posts = [
    path('list/', apis.PostList.as_view()),
    path('', apis.PostDetail.as_view()),

    path('create/', apis.PostCreateAPIView.as_view()),

    path('image/', apis.PostImageView.as_view()),
    # path('deberg-test/', views.deberg_test),
    # path('postFiltering/', apis.PostFiltering.as_view()),

    # 전영훈 urls -----
    path('bjd/', apis.getAptListService),
    path('bc/', getBorodCityList),
    path('sg/', getSiGunGuList),
    path('emd/', getEupMyunDongList),
    path('test/', test),
]
