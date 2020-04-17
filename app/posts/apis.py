import json
import urllib.request as ul
from io import BytesIO
from xml.etree.ElementTree import XMLParser

import xmltodict
import requests
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import PostRoom, PostImage
from posts.serializers import PostListSerializer, PostImageSerializer

secret = 's8%2FOL9BcK3JUYuSOOnFxFN%2B342crXBDe08GV9iRCN536y1XDkmU4KKKNUaf79BbPODPv9Lj%2BRZ4IYu3ynJ4VWA%3D%3D'


class PostList(APIView):
    # 게시물 생성 : /posts/
    def post(self, request, format=None):
        serializer = PostListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 게시물 조회 : /posts/
    def get(self, request, format=None):
        queryset = PostRoom.objects.all()
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)


class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return PostRoom.objects.get(pk=pk)
        except PostRoom.DoesNotExist:
            raise Http404

    # 특정 게시물 조회 : /posts/{pk}/
    def get(self, request, pk):
        postroom = self.get_object(pk)
        serializer = PostListSerializer(postroom)
        return Response(serializer.data)

    # 특정 게시물 수정 : /posts/{pk}/
    def put(self, request, pk, format=None):
        postroom = self.get_object(pk)
        serializer = PostListSerializer(postroom, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 특정 게시물 삭제 : /posts/{pk}/
    def delete(self, request, pk, format=None):
        postroom = self.get_object(pk)
        postroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostImageView(APIView):
    def get(self, request):
        queryset = PostImage.objects.all()
        serializer = PostImageSerializer(queryset, many=True)
        return Response(serializer.data)


def AptListService(request):
    url_road = \
        'http://apis.data.go.kr/1611000/AptListService/getRoadnameAptList?' \
        'roadCode=263802006002' \
        '&ServiceKey=s8%2FOL9BcK3JUYuSOOnFxFN%2B342crXBDe08GV9iRCN536y1XDkmU4KKKNUaf79BbPODPv9Lj%2BRZ4IYu3ynJ4VWA%3D%3D'

    url_bjd = \
        'http://apis.data.go.kr/1611000/AptListService/getLegaldongAptList?' \
        'bjdCode=2638010100' \
        '&ServiceKey=s8%2FOL9BcK3JUYuSOOnFxFN%2B342crXBDe08GV9iRCN536y1XDkmU4KKKNUaf79BbPODPv9Lj%2BRZ4IYu3ynJ4VWA%3D%3D'
    response = requests.get(url_bjd).content
    # print(response.status_code)
    xmlObj = xmltodict.parse(response)
    print(xmlObj)
    pass


@api_view()
def getBorodCityList(request):
    url = f'http://openapi.epost.go.kr/postal/retrieveLotNumberAdressAreaCdService/' \
          f'retrieveLotNumberAdressAreaCdService/getBorodCityList?ServiceKey={secret}'
    response = requests.get(url).content
    xmlObj = xmltodict.parse(response)
    json_data = json.dumps(xmlObj, ensure_ascii=False)
    dict_data = json.loads((json_data))
    data = dict_data["BorodCityResponse"]["borodCity"]
    return Response(data, status=status.HTTP_200_OK)


@api_view()
def getSiGunGuList(request):
    brtcCd = request.data.get('brtcCd')
    url = f'http://openapi.epost.go.kr/postal/retrieveLotNumberAdressAreaCdService/' \
          f'retrieveLotNumberAdressAreaCdService/getSiGunGuList?ServiceKey={secret}&brtcCd={brtcCd}'
    response = requests.get(url).content
    xmlObj = xmltodict.parse(response)
    json_data = json.dumps(xmlObj, ensure_ascii=False)
    dict_data = json.loads((json_data))
    error = dict_data['SiGunGuListResponse']['cmmMsgHeader']['successYN']
    if error == 'N':
        data = {
            'message': '데이터가 올바르지 않습니다.'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    data = dict_data['SiGunGuListResponse']['siGunGuList']
    return Response(data, status=status.HTTP_200_OK)


@api_view()
def getEupMyunDongList(request):
    brtcCd = request.data.get('brtcCd')
    signguCd = request.data.get('signguCd')
    url = f'http://openapi.epost.go.kr/postal/retrieveLotNumberAdressAreaCdService/' \
          f'retrieveLotNumberAdressAreaCdService/getEupMyunDongList?ServiceKey={secret}' \
          f'&brtcCd={brtcCd}&signguCd={signguCd}'
    response = requests.get(url).content
    xmlObj = xmltodict.parse(response)
    json_data = json.dumps(xmlObj, ensure_ascii=False)
    dict_data = json.loads((json_data))
    error = dict_data['EupMyunDongListResponse']['cmmMsgHeader']['successYN']
    if error == 'N':
        data = {
            'message': '데이터가 올바르지 않습니다.'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    data = dict_data['EupMyunDongListResponse']['eupMyunDongList']
    return Response(data, status=status.HTTP_200_OK)
