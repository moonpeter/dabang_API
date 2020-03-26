from django.contrib.auth.models import AbstractUser
from django.db import models

from posts.models import PostRoom


class User(AbstractUser):
    introduce = models.TextField(max_length=100)
    social = models.ManyToManyField(
        'SocialLogin',
    )
    post = models.ManyToManyField(
        PostRoom,
    )


class SocialLogin(models.Model):
    type = models.CharField(max_length=10, )

    def __str__(self):
        return self.type

    def __repr__(self):
        return self.type