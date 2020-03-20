import jwt
import requests
from django.contrib.auth import get_user_model
from requests import Response
from rest_framework import permissions
from rest_framework.views import APIView

from config.settings import SECRET_KEY
from members.serializers import UserSerializer

User = get_user_model()


class KakaoJwtTokenView(APIView):
    def post(self, request):
        return Response(request.data)
        # url = 'https://kapi.kakao.com/v2/user/me'
        #
        # headers = {
        #     'Authorization': f'Bearer {access_token}',
        #     'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        # }
        # kakao_response = requests.post(url, headers=headers)
        #
        # user_data = kakao_response.json()
        # kakao_id = user_data['id']
        # user_username = user_data['properties']['nickname']
        # user_first_name = user_username[1:]
        # user_last_name = user_username[0]
        #
        # # kakao_user_image = user_data['properties']['profile_image']
        # # img_response = requests.get(kakao_user_image)
        # # img_data = img_response.content
        # # ext = imghdr.what('', h=img_data)
        # # f = SimpleUploadedFile(f'{kakao_id}.{ext}', img_response.content)
        #
        # jwt_token = jwt.encode({'id': kakao_id, 'username': kakao_id, }, SECRET_KEY, algorithm='HS256').decode('UTF-8')
        #
        # try:
        #     user = User.objects.get(username=kakao_id)
        #
        # except User.DoesNotExist:
        #     user = User.objects.create_user(
        #         username=kakao_id,
        #         first_name=user_first_name,
        #         last_name=user_last_name,
        #     )
        # data = {
        #     'token': jwt_token,
        #     'user': UserSerializer(user).data,
        # }
        #
        # return Response(data)


class FacebookJwtToken(APIView):
    api_base = 'https://graph.facebook.com/v3.2'
    api_get_access_token = f'{api_base}/oauth/access_token'
    api_me = f'{api_base}/me'

    def post(self, request, access_token):
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
        # url_image = data['picture']['data']['url']
        # # http get 요청의 응답을 받아와서, binary data 를 img_data 에 할당
        # img_response = requests.get(url_image)
        # img_data = img_response.content

        # 응답의 binary data를 사용해서, in-memory binary stream(file) 객체를 생성,
        # f = io.ByteIO(img_response.content)

        # FileField가 지원하는 InMemoryUploadedFile 객체를 사용하기,
        # imghdr 모듈을 사용해서 페이스북에서 받은 파일 확장자를 확인
        # ext = imghdr.what('', h=img_data)
        # f = SimpleUploadedFile(f'{facebook_id}.{ext}', img_response.content)

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

# class MyProfileView(APIView):
#     permission_classes = (
#         permissions.IsAuthenticated,
#     )
#
#     def get(self, request):
#         user = request._user
#         serializer = UserProfileSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request):
#         user = request._user
#         serializer = UserProfileChangeSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)