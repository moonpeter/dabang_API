# Generated by Django 2.2.11 on 2020-04-05 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postroom',
            name='parkingTF',
            field=models.BooleanField(default=True, verbose_name='주차 가능 유무'),
            preserve_default=False,
        ),
    ]
