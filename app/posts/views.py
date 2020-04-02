from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import PostRoom
from posts.serializers import PostCreateSerializer


class PostListAPIView(APIView):
    def get(self, request):
        serializer = PostCreateSerializer(PostRoom.objects.all(), many=True)

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
