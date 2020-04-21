from django.urls import path

from posts import apis, views

urlpatterns_posts = [
    path('', apis.PostList.as_view()),
    path('<int:pk>/', apis.PostDetail.as_view()),
    path('image/', apis.PostImageView.as_view()),
    # path('deberg-test/', views.deberg_test),
    # path('postFiltering/', apis.PostFiltering.as_view()),
]
