import imghdr

import jwt
import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from requests import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from config.settings import SECRET_KEY, KAKAO_APP_ID
from members.serializers import UserSerializer

User = get_user_model()


def login_page(request):
    context = {
        'user': request.user
    }
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('login-page')


def facebook_login(request):
    api_base = 'https://graph.facebook.com/v3.2'
    api_get_access_token = f'{api_base}/oauth/access_token'
    api_me = f'{api_base}/me'

    # user = authenticate(request, facebook_request_token=request.GET.get('code'))
    code = request.GET.get('code')

    # request token을 access token으로 교환
    params = {
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': 'http://localhost:8000/members/facebook-login/',
        'client_secret': settings.FACEBOOK_APP_SECRET,
        'code': code,
    }
    response = requests.get(api_get_access_token, params)
    # 인수로 전달한 문자열이 'JSON'형식일 것으로 생각
    # json.loads는 전달한 문자열이 JSON형식일 경우, 해당 문자열을 parsing해서 파이썬 Object를 리턴함
    # response_object = json.loads(response.text)
    data = response.json()
    access_token = data['access_token']
    print('access token', access_token)
    params = {
        'access_token': access_token,
        'fields': ','.join([
            'id',
            'first_name',
            'last_name',
            # 'picture.type(large)',
        ])
    }
    response = requests.get(api_me, params)
    data = response.json()

    facebook_id = data['id']
    first_name = data['first_name']
    last_name = data['last_name']

    jwt_token = jwt.encode({'username': facebook_id}, SECRET_KEY, algorithm='HS256').decode('utf-8')

    try:
        user = User.objects.get(username=facebook_id)
        user.last_name = last_name
        user.first_name = first_name
        user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=facebook_id,
            first_name=first_name,
            last_name=last_name,
        )
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return HttpResponse(f'id: {facebook_id}, jwt: {jwt_token}, access_token: {access_token}')


def kakao_login(request):
    kakao_access_code = request.GET.get('code')
    url = 'https://kauth.kakao.com/oauth/token'
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    body = {
        'grant_type': 'authorization_code',
        'client_id': KAKAO_APP_ID,
        'redirect_url': 'https://moonpeter.com/members/kakao-login/',
        'code': kakao_access_code
    }
    kakao_reponse = requests.post(url, headers=headers, data=body)
    #  front 에서 받아야 할 역할 완료 /

    data = kakao_reponse.json()
    access_token = data['access_token']
    print(access_token)
    url = 'https://kapi.kakao.com/v2/user/me'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    kakao_response = requests.post(url, headers=headers)

    user_data = kakao_response.json()
    kakao_id = user_data['id']
    user_username = user_data['properties']['nickname']
    print(type(user_username))
    user_first_name = user_username[1:]
    user_last_name = user_username[0]

    jwt_token = jwt.encode({'id': kakao_id, 'username': kakao_id, }, SECRET_KEY, algorithm='HS256').decode('UTF-8')

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
        'user': UserSerializer
    }
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    # return redirect('login-page')
    return HttpResponse(f'username: {kakao_id} token:{jwt_token} access_token:{access_token}')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

