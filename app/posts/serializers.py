from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from .models import PostRoom, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    broker = StringRelatedField(read_only=True)
    management = StringRelatedField(many=True, read_only=True)
    option = StringRelatedField(many=True, read_only=True)
    securitySafety = StringRelatedField(many=True, read_only=True)
    address = StringRelatedField(read_only=True)
    salesForm = StringRelatedField(read_only=True)
    postimages = StringRelatedField(source='postimage_set', many=True)

    class Meta:
        model = PostRoom
        fields = [
            'id',
            'description',
            'floor',
            'totalFloor',
            'areaChar',
            'supplyAreaInt',
            'supplyAreaChar',
            'shortRent',
            'parkingDetail',
            'parkingTF',
            'living_expenses',
            'living_expenses_detail',
            'moveInChar',
            'moveInDate',
            'heatingType',
            'pet',
            'elevator',
            'builtIn',
            'veranda',
            'depositLoan',
            'broker',
            'address',  #
            'salesForm',  #
            'management',  #
            'option',  #
            'securitySafety',  #
            'postimages',
        ]
