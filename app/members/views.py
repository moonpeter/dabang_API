from django.contrib.auth import get_user_model, authenticate
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from members.serializers import UserSerializer, UserLoginSerializer, UserProfileSerializer
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()


class UserViewSet(viewsets.ViewSet):
    """
    viewsets.ViewSet 특징
    - 반복된 논리를 단일 클래스로 결합
    - 라우터를 사용하여 URL conf 직접 배선하지 않아도 되는 편리함
    # 단점
    - 모든 메서드 직접 구현
    """

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_authenticate_header(self, request):
        authentication_classes = [JSONWebTokenAuthentication]
        return [authenticate() for authenticate in authentication_classes]

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(
            username=username,
            password=password,
        )
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_patch(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserModelViewSet(viewsets.ModelViewSet):
    """
    viewsets.ModelViewSet 특징
    'list', 'create', 'retrieve', 'update', 'destroy' 기능 자동 지원, 별도의 함수 작성 가능 api코드 간소화

    # 함수들을 오버라이딩 하는 경우 상속받는 기능의 코드를 이해한 상태에서 건드려야 생산성과 유지보수의 이점을 둘 다 가져가는 듯 하다.
    # 각 함수를 오버라이딩 할 때 어떤 모듈의 함수인지 이해하는 지식 필요할 듯

    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        if self.action in "create":
            serializer_class = UserSerializer
        else:
            serializer_class = UserProfileSerializer
        return serializer_class

    def get_permissions(self):
        permission_classes = super().get_permissions()
        if self.action == ("retrieve", "partial_update", "update", "destroy"):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_authenticate_header(self, request):
        authentication_classes = [JSONWebTokenAuthentication]
        return [authentication() for authentication in authentication_classes]

    @action(detail=False, methods=['POST'])
    def jwt(self, request):
        username = request.POST.get('email')
        userpass = request.POST.get('password')
        user = authenticate(username=username, password=userpass)
        payload = JWT_PAYLOAD_HANDLER(user)
        jwt_token = JWT_ENCODE_HANDLER(payload)
        if user is not None:
            data = {
                'jwt': jwt_token,
                'user': UserSerializer(user).data
            }
            return Response(data)


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
    permission_classes = (IsAuthenticated,)
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
