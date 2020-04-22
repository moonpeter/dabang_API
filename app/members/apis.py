import json

import jwt
import requests
from django.conf.global_settings import SECRET_KEY
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views import View
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action

from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import KAKAO_APP_ID, FACEBOOK_APP_SECRET, FACEBOOK_APP_ID
from members.serializers import UserSerializer, UserProfileSerializer

User = get_user_model()


class UserModelViewSet(viewsets.ModelViewSet):
    """
    viewsets.ModelViewSet 특징
    'list', 'create', 'retrieve', 'update', 'destroy' 기능 자동 지원, 별도의 함수 작성 가능 api코드 간소화

    # 함수들을 오버라이딩 하는 경우 상속받는 기능의 코드를 이해한 상태에서 건드려야 생산성과 유지보수의 이점을 둘 다 가져가는 듯 하다.
    # 각 함수를 오버라이딩 할 때 어떤 모듈의 함수인지 이해하는 지식 필요할 듯

    추후 추가할 기능들
     - 유저 프로필 페이지 최근 본 게시글 목록, 찜한 게시글 목록
     - 회원가입 시 유저 아이디 중복 체크
     - 유저 패스워드 변경
     - 특정 상황에 따른 푸쉬알림
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_class(self):
        if self.action in "create":
            serializer_class = UserSerializer
            return serializer_class
        else:
            serializer_class = UserProfileSerializer
            return serializer_class

    def get_permissions(self):
        if self.action == ("retrieve", "partial_update", "update", "destroy"):
            permission_classes = [IsAuthenticated()]
            return permission_classes
        elif self.action == "list":
            # 모든 유저의 목록을 보여주고 싶지 않아서
            permission_classes = [IsAdminUser()]
            return permission_classes
        else:
            permission_classes = [AllowAny()]
            return permission_classes


class socialLogin(APIView):
    def post(self, request):
        local_host = 'http://localhost:8000'
        deploy_host = 'https://moonpeter.com'
        url = f'{local_host}/auth/convert-token'
        token = request.data.get('token')
        social_type = request.data.get('type')
        if social_type:
            if social_type == 'facebook':
                client_id = FACEBOOK_APP_ID
                client_pass = FACEBOOK_APP_SECRET
            elif social_type == 'kakao':
                client_id = KAKAO_APP_ID

        params = {
            "grant_type": "convert_token",
            "client_id": f"{client_id}",
            "backend": f'{social_type}',
            "token": f'{token}'
        }
        if social_type == 'facebook':
            params["client_secret"] = client_pass

        response = requests.post(url, params=params)

        response_json = response.json()

        data = {
            'res': response_json,
        }
        return Response(data, status=status.HTTP_200_OK)
