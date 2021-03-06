import json

import requests
import xmltodict
from django.http import Http404
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import PostLike
from posts.models import PostRoom, PostImage, ComplexInformation
from posts.serializers import PostLIkeSerializer, UploadImageSerializer, SalesFormSerializer
from posts.serializers import PostListSerializer, PostImageSerializer, AddressSerializer, PostCreateSerializer, \
    ComplexInformationSerializer

secret = 'V8giduxGZ%2BU463maB552xw3jULhTVPrv%2B7m2qSqu4w8el9fk8bnMD9i6rjUQz7gcUcFnDKyOmcCBztcbVx3Ljg%3D%3D'


@api_view()
def ComplexAPIView(request):
    queryset = ComplexInformation.objects.all()
    serializer = ComplexInformationSerializer(queryset, many=True, )
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view()
def ComplexDetail(request):
    pk = request.query_params.get('pk')
    if pk:
        complex_ins = ComplexInformation.objects.get(pk=pk)
        serializer = ComplexInformationSerializer(complex_ins)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        data = {
            'message': '존재하지 않는 단지 정보 입니다.'
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)


@api_view()
def ComplexDetail(request):
    pk = request.query_params.get('pk')
    if pk:
        complex_ins = ComplexInformation.objects.get(pk=pk)
        serializer = ComplexInformationSerializer(complex_ins)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        data = {
            'message': '존재하지 않는 단지 정보 입니다.'
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)


class PostList(generics.ListCreateAPIView):
    model = PostRoom
    serializer_class = PostListSerializer
    queryset = PostRoom.objects.all()
    parser_class = (FileUploadParser,)

    # 게시물 조회 : /posts/
    def get(self, request, format=None):
        queryset = PostRoom.objects.all()
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)


class PostDetail(RetrieveAPIView):
    serializer_class = PostListSerializer

    def get_object(self):
        pk = self.request.query_params.get('pk', None)
        try:
            return PostRoom.objects.get(pk=pk)
        except PostRoom.DoesNotExist:
            raise Http404

    def get_queryset(self):
        self.request.query_params.get()

    # # 특정 게시물 조회 : /posts/{pk}/
    # def get(self, request, pk):
    #     postroom = self.get_object(pk)
    #     serializer = PostListSerializer(postroom)
    #     return Response(serializer.data)

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


class PostLikeView(RetrieveAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, post_pk):
        post = get_object_or_404(PostRoom, pk=post_pk)
        serializer = PostLIkeSerializer(
            data={**request.data, 'post': post_pk}
        )
        if serializer.is_valid():
            if PostLike.objects.filter(
                    post=serializer.validated_data['post'],
                    user=request.user,
            ).exists():
                raise APIException('이미 좋아요 한 포스트 입니다.')
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_pk):
        post = get_object_or_404(PostRoom, pk=post_pk)
        post_like = get_object_or_404(PostLike, post=post, user=request.user)
        post_like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageUploadView(APIView):
    # parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        image_serializer = UploadImageSerializer(data=request.data)
        if image_serializer.is_valid():
            image_serializer.save()
            return Response(image_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            # address 객체 생성
            address_serializer = AddressSerializer(data=request.data.get('address'))
            if address_serializer.is_valid():
                address = address_serializer.save()

            # salesform 객체 생성
            salesform_serializer = SalesFormSerializer(data=request.data.get('salesForm'))
            if salesform_serializer.is_valid():
                salesForm = salesform_serializer.save()

            serializer.save(address=address, salesForm=salesForm)

            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)