from rest_framework import serializers

from .models import PostTest, PostRoom


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostRoom
        # fields = '__all__'
        fields = (
            'description',
            'pk',
        )

# TestSerializer
class PostListTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTest
        # fields = '__all__'
        fields = (
            'testtitle',
            'testdesc',
            'pk',
        )
