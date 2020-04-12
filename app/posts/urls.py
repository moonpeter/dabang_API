from django.urls import path

from posts import apis

urlpatterns_posts = [
    path('', apis.PostList.as_view()),
    path('<int:pk>/', apis.PostDetail.as_view()),
    path('image/', apis.PostImageView.as_view()),
]