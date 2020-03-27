from django.contrib.auth.models import AbstractUser

import posts


from django.db import models

from posts.models import PostLike


class User(AbstractUser):
    introduce = models.TextField(max_length=100)
    social = models.ManyToManyField(
        'SocialLogin',
    )
    post = models.ManyToManyField(
        posts.models.PostRoom,
        through=PostLike,
    )


class SocialLogin(models.Model):
    type = models.CharField(max_length=10, )

    def __str__(self):
        return self.type

    def __repr__(self):
        return self.type
