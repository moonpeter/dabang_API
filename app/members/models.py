from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    introduce = models.TextField(max_length=100)
    social = models.ManyToManyField(
        'members.SocialLogin',
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
