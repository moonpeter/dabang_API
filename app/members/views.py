from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from members.permissions import IsOwnerOrReadOnly

from members.serializers import UserSerializer, UserProfileSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Generic API View 를 상속하며, .list(), .retrieve(), .create(), .update(), .partial_update(), .destroy() action 지원.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'partial_update':
            permission_classes = [IsOwnerOrReadOnly]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         serializer_class = UserSerializer
    #     else:
    #         serializer_class = UserProfileSerializer
