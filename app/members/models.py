from django.contrib.auth.models import AbstractUser
from django.db import models

from config import settings
from posts.models import PostRoom


def user_image_path(instance, filename):
    a = f'{instance.id}/{filename}'
    return a


# Create your models he re.
class User(AbstractUser):
    social = models.ManyToManyField(
        'members.SocialLogin',
    )
    phone = models.CharField('핸드폰', max_length=15, null=True, default=True)
    profileImage = models.ImageField(
        '유저 이미지',
        null=True,
        default='userImages.png'
    )
    posts = models.ManyToManyField(
        PostRoom,
        through='RecentlyPostList',
    )


class SocialLogin(models.Model):
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.type

    def __repr__(self):
        return self.type

    @staticmethod
    def start():
        socials = ['kakao', 'facebook', 'apple']
        for i in socials:
            SocialLogin.objects.create(
                type=i,
            )


class RecentlyPostList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='유저',
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        PostRoom,
        verbose_name='게시글',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True, )
