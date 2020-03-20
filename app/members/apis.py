import jwt
import requests
from django.contrib.auth import get_user_model
from requests import Response
from rest_framework.views import APIView

from config.settings import SECRET_KEY
from members.serializers import UserSerializer

User = get_user_model()


class KakaoJwtTokenView(APIView):
    def post(self, request, access_token):
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

        # kakao_user_image = user_data['properties']['profile_image']
        # img_response = requests.get(kakao_user_image)
        # img_data = img_response.content
        # ext = imghdr.what('', h=img_data)
        # f = SimpleUploadedFile(f'{kakao_id}.{ext}', img_response.content)

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
            'user': UserSerializer(user).data,
        }

        return Response(data)
