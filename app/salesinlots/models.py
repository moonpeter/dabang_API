from django.db import models

# Create your models here.


class CrawlingData(models.Model):
    link = models.URLField()