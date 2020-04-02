from django.urls import path

from posts import apis, views

urlpatterns_posts = [
    path('create/', views.PostListAPIView.as_view()),
]