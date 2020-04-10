from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from .models import PostRoom


# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PostAddress
#         fields = [
#             'loadAddress',
#             'detailAddress',
#         ]


class PostListSerializer(serializers.ModelSerializer):
    broker = StringRelatedField(read_only=True)
    management = StringRelatedField(many=True, read_only=True)
    option = StringRelatedField(many=True, read_only=True)
    securitySafety = StringRelatedField(many=True, read_only=True)
    address = StringRelatedField(read_only=True )
    salesForm = StringRelatedField(read_only=True)

    class Meta:
        model = PostRoom
        fields = [
                'id',
                'description',
                'floor',
                'totalFloor',
                'areaInt',
                'areaChar',
                'supplyAreaInt',
                'supplyAreaChar',
                'shortRent',
                'parkingDetail',
                'parkingTF',
                'living_expenses',
                'living_expenses_detail',
                'MoveInChar',
                'moveInDate',
                'heatingType',
                'pet',
                'elevator',
                'multiFloor',
                'pointRoom',
                'builtIn',
                'veranda',
                'depositLoan',
                'broker',
                'address', #
                'salesForm', #
                'management', #
                'option', #
                'securitySafety', #
        ]


