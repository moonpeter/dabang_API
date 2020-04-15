import json
import urllib.request as ul
from io import BytesIO
from xml.etree.ElementTree import XMLParser

import xmltodict
import requests
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import PostRoom, PostImage
from posts.serializers import PostListSerializer, PostImageSerializer


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


def apiTestCode(request):
    import urllib
    from pprint import pprint

    # headers = {
    #     'serviceKey': 's8%2FOL9BcK3JUYuSOOnFxFN%2B342crXBDe08GV9iRCN536y1XDkmU4KKKNUaf79BbPODPv9Lj%2BRZ4IYu3ynJ4VWA%3D%3D',
    #     'roadCode': '263802006002',
    #     'pageNo': 1,
    #     'numOfRows': 10
    # }
    # =====================================
    url = 'http://apis.data.go.kr/1611000/AptListService/getRoadnameAptList?serviceKey=s8%2FOL9BcK3JUYuSOOnFxFN%2' \
          'B342crXBDe08GV9iRCN536y1XDkmU4KKKNUaf79BbPODPv9Lj%2BRZ4IYu3ynJ4VWA%3D%3D' \
          '&roadCode=263802006002&pageNo=1&numOfRows=10'
    # request = ul.Request(url)
    # response = ul.urlopen(request)
    # rescode = response.getcode()
    #
    # if (rescode == 200):
    #     responseData = response.read()
    #
    #     rD = xmltodict.parse(responseData)
    #     # rD = rD.decode('utf-8')
    #     rDJ = json.dumps(rD)
    #     rDD = json.dumps(rDJ)
    #     print(rDD)
    request = requests.get(url).content
    xmlObj = xmltodict.parse(request)
    # allData = xmltodict['response']['body']['items']
    pass
