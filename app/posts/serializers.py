from rest_framework import serializers
from rest_framework.fields import DictField, CharField, ListField
from rest_framework.relations import StringRelatedField

from .models import PostRoom, PostImage, Broker, MaintenanceFee, RoomOption, PostAddress, RoomSecurity, SalesForm, \
    OptionItem, SecuritySafetyFacilities, PostLike, UploadImage


class BrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broker
        fields = (
            'pk', 'companyName', 'address', 'managerName', 'tel', 'image', 'companyNumber', 'brokerage',
            'dabangCreated_at', 'successCount'
        )

    # def create(self, validated_data):
    #     broker = validated_data.pop('broker')
    #     instance = Broker.objects.create(**validated_data)
    #     return instance
    # def create(self, validated_data):
    #     return Broker.objects.get_or_create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.address = validated_data.get('address', instance.address)
    #     instance.manager = validated_data.get('manager', instance.manager)
    #     instance.tel = validated_data.get('tel', instance.tel)
    #     instance.save()
    #     return instance


class ManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceFee
        fields = (
            'postRoom', 'admin', 'totalFee',
        )


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionItem
        fields = (
            'name',
        )


class SecuritySafetySerializer(serializers.ModelSerializer):
    class Meta:
        model = SecuritySafetyFacilities
        fields = (
            'name',
        )


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAddress
        fields = (
            'loadAddress', 'detailAddress',
        )


class SalesFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesForm
        fields = (
            'type', 'depositChar', 'monthlyChar', 'depositInt', 'monthlyInt',
        )


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = (
            'image',
        )


class PostListSerializer(serializers.ModelSerializer):
    broker = BrokerSerializer(read_only=True)
    management_set = serializers.StringRelatedField(source='management', many=True, read_only=True)
    option_set = serializers.StringRelatedField(source='option', many=True, read_only=True)
    securitySafety_set = serializers.StringRelatedField(source='securitySafety', many=True, read_only=True)
    address = AddressSerializer(read_only=True, allow_null=True)
    salesForm = SalesFormSerializer(read_only=True)
    postimage = serializers.StringRelatedField(read_only=True, source='postimage_set', many=True)

    class Meta:
        model = PostRoom
        fields = [
            'pk',
            'broker',
            'type',
            'description',
            'address',
            'lng',
            'lat',
            'salesForm',
            'floor',
            'totalFloor',
            'areaChar',
            'supplyAreaInt',
            'supplyAreaChar',
            'shortRent',
            'management_set',
            'parkingDetail',
            'parkingTF',
            'living_expenses',
            'living_expenses_detail',
            'moveInChar',
            'moveInDate',
            'option_set',
            'heatingType',
            'pet',
            'elevator',
            'builtIn',
            'veranda',
            'depositLoan',
            'totalCitizen',
            'totalPark',
            'complete',
            'securitySafety_set',
            'postimage',
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    # address = DictField(child=CharField(), allow_empty=True, )
    address = AddressSerializer(read_only=True)
    salesForm = DictField(source='salesform_set', child=CharField(), read_only=True)
    # salesForm = SalesFormSerializer(source='salesform_set', required=False, many=True)
    management_set = ListField()
    option_set = ListField()
    securitySafety_set = ListField()

    class Meta:
        model = PostRoom
        # fields = '__all__'
        fields = [
            'pk',
            'broker',
            'type',
            'description',
            'salesForm',
            'floor',
            'totalFloor',
            'areaChar',
            'supplyAreaInt',
            'supplyAreaChar',
            'shortRent',
            'management_set',
            'parkingDetail',
            'parkingTF',
            'living_expenses',
            'living_expenses_detail',
            'moveInChar',
            'moveInDate',
            'option_set',
            'heatingType',
            'pet',
            'elevator',
            'builtIn',
            'veranda',
            'depositLoan',
            'totalCitizen',
            'totalPark',
            'complete',
            'securitySafety_set',
            'address',
            # 'postimage',
        ]


class PostLIkeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = [
            'post',
            'user',
        ]


class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadImage
        fields = (
            'image',
        )