#
#
# class PostCreateView(generics.CreateAPIView):
#     serializer_class = PostCreateSerializer
#
#     def create(self, request, *args, **kwargs):
#
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#
#             address_serializer = AddressSerializer(data=request.data.get('address'))
#             if address_serializer.is_valid():
#                 address = address_serializer.save()
#
#             salesform_serializer = SalesFormSerializer(data=request.data.get('salesForm'))
#             if salesform_serializer.is_valid():
#                 salesform = salesform_serializer.save()
#
#             serializer.save(address=address, salesForm=salesForm)
#
#             return Response(satus=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)