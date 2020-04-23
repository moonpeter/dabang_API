import json
import xmltodict
import requests
from django.http import Http404, HttpResponse
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

# from posts.filters import PostRoomFilter
from posts.models import PostRoom, PostImage, PostAddress
from posts.serializers import PostListSerializer, PostImageSerializer, AddressSerializer

secret = 'V8giduxGZ%2BU463maB552xw3jULhTVPrv%2B7m2qSqu4w8el9fk8bnMD9i6rjUQz7gcUcFnDKyOmcCBztcbVx3Ljg%3D%3D'


# class PostRoomViewSet(viewsets.ModelViewSet):
#     serializer_class = PostListSerializer
#     queryset = PostRoom.objects.all()
#     print(PostListSerializer)
#
#
# class PostAddressViewSet(viewsets.ModelViewSet):
#     serializer_class = AddressSerializer
#     queryset = PostAddress.objects.all()


class PostList(generics.ListCreateAPIView):
    model = PostRoom
    serializer_class = PostListSerializer
    queryset = PostRoom.objects.all()
    parser_class = (FileUploadParser,)

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
    def patch(self, request, pk, format=None):
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


@api_view()
def getAptListService(request):
    secret_key = 'V8giduxGZ%2BU463maB552xw3jULhTVPrv%2B7m2qSqu4w8el9fk8bnMD9i6rjUQz7gcUcFnDKyOmcCBztcbVx3Ljg%3D%3D'
    url = "http://apis.data.go.kr/1611000/AptListService/getLegaldongAptList"
    bjd_code = request.data.get('bjdCode')
    if bjd_code == '성수동1가':
        bjd_code = '1120011400'
    elif bjd_code == '성수동2가':
        bjd_code = '1120011500'

    url_bjd = f'{url}?bjdCode={bjd_code}&ServiceKey={secret_key}'

    response = requests.get(url_bjd).content

    xmlObj = xmltodict.parse(response)
    json_data = json.dumps(xmlObj, ensure_ascii=False)
    dict_data = json.loads((json_data))
    data = dict_data['response']['body']['items']['item']
    return Response(data, status=status.HTTP_200_OK)


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
