import jwt
import requests
from django.contrib.auth import get_user_model, authenticate
from rest_framework import permissions, status

from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import SECRET_KEY
from members.permissions import IsOwnerOrReadOnly
from members.serializers import UserSerializer, UserProfileSerializer, SignUpViewSerializer

User = get_user_model()


class KakaoJwtTokenView(APIView):
    def post(self, request):
        access_token = request.POST.get('access_token')
        url = 'https://kapi.kakao.com/v2/user/me'
        access_token = request.data.get('access_token')
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        kakao_response = requests.post(url, headers=headers)

        user_data = kakao_response.json()
        kakao_id = user_data['id']
        user_username = user_data['properties']['nickname']
        user_first_name = user_username[1:]
        user_last_name = user_username[0]
        jwt_token = jwt.encode({'username': kakao_id}, SECRET_KEY, algorithm='HS256').decode('UTF-8')

        try:
            user = User.objects.get(username=kakao_id)

        except User.DoesNotExist:
            user = User.objects.create_user(

                username=kakao_id,
                first_name=user_first_name,
                last_name=user_last_name,
            )
        data = {
            'token': jwt_token,
            'user': UserSerializer(user).data,
        }

        return Response(data)


class FacebookJwtToken(APIView):
    api_base = 'https://graph.facebook.com/v3.2'
    api_get_access_token = f'{api_base}/oauth/access_token'
    api_me = f'{api_base}/me'

    def post(self, request):
        access_token = request.POST.get('access_token')
        params = {
            'access_token': access_token,
            'fields': ','.join([
                'id',
                'first_name',
                'last_name',
                'picture.type(large)',
            ])
        }
        response = requests.get(self.api_me, params)
        data = response.json()

        facebook_id = data['id']
        first_name = data['first_name']
        last_name = data['last_name']

        jwt_token = jwt.encode({'username': facebook_id}, SECRET_KEY, algorithm='HS256').decode('utf-8')

        try:
            user = User.objects.get(username=facebook_id)
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=facebook_id,
                first_name=first_name,
                last_name=last_name,
                # img_profile=f,
            )
        data = {
            'token': jwt_token,
            'user': UserSerializer(user).data,
        }
        return Response(data)


class MyProfileView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    def get(self, request):
        user = request._user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request._user
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserJwtToken(APIView):
    def post(self, request):
        username = request.POST.get('email')
        userpass = request.POST.get('password')
        user = authenticate(username=username, password=userpass)
        jwt_token = jwt.encode({'username': username}, SECRET_KEY, algorithm='HS256').decode('utf-8')
        if user is not None:
            data = {
                'jwt': jwt_token,
                'user': UserSerializer(user).data
            }
            return Response(data)


class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpViewSerializer(data=request.data)
        if serializer.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            User.objects.create_user(
                username=username,
                password=password,
                email=email,
            )
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)