from django.contrib.auth import get_user_model
from rest_framework import serializers, permissions

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            # 'password',
            'introduce',
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()
    serializers_class = UserSerializer
    permissions_classes = (permissions.IsAuthenticated,)

    class Meta:
        model = User
        fields = [
            'introduce'
        ]
