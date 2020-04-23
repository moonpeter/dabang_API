# from rest_framework import viewsets
#
# from posts.models import PostRoom
# from posts.serializers import PostListSerializer
#
#
# class PostRoomViewSet(viewsets.ModelViewSet):
#     serializer_class = PostListSerializer
#
#     def get_queryset(self):
#         return PostRoom.objects.all()
#
#     def perform_create(self, serializer):
#         serializer.save()
