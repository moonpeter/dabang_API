from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from members.permissions import IsOwnerOrReadOnly

from members.serializers import UserSerializer, UserLoginSerializer

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


class UserLoginView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token': serializer.data['token'],
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class UserProfileView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request):
        try:
            user = User.objects.get(username=request.user.username)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'username': user.username,
                    'email': user.email,
                    'introduce': user.introduce,
                }]
            }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
            }
        return Response(response, status=status_code)
