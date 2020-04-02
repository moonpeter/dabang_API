from rest_framework import serializers

from .models import PostRoom


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostRoom
        fields = '__all__'
