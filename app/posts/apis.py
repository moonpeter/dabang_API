from django.http import Http404
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

# from posts.filters import PostRoomFilter
from posts.models import PostRoom, PostImage, PostAddress
from posts.serializers import PostListSerializer, PostImageSerializer, AddressSerializer


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
