from django.conf.urls import url
from django.urls import path, re_path

from posts import apis, views
from posts.apis import getBorodCityList, getEupMyunDongList, getSiGunGuList

urlpatterns_posts = [
    path('', apis.PostList.as_view()),
    # path('<int:pk>/', apis.PostDetail.as_view()),
    re_path(r'^(?P<pk>\d+)/$', apis.PostDetail.as_view()),

    path('image/', apis.PostImageView.as_view()),
    # path('deberg-test/', views.deberg_test),
    # path('postFiltering/', apis.PostFiltering.as_view()),
    path('bjd/', apis.getAptListService),
    path('bc/', getBorodCityList),
    path('sg/', getSiGunGuList),
    path('emd/', getEupMyunDongList),
]
