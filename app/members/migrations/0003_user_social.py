# Generated by Django 3.0.5 on 2020-04-23 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_sociallogin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='social',
            field=models.ManyToManyField(to='members.SocialLogin'),
        ),
    ]
