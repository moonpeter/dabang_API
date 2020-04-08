from django.urls import path

from posts import apis

urlpatterns_posts = [
    path('', apis.PostList.as_view()),
    path('<int:pk>/', apis.PostDetail.as_view()),
    path('posttest/', apis.PostListTest.as_view()), # test용
    path('posttest/<int:pk>/', apis.PostDetailTest.as_view()),  # test용
]