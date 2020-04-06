from rest_framework import serializers

from .models import PostTest


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTest
        fields = (
            'testtitle',
        )
