from django.db import models
from config import settings


class PostRoom(models.Model):
    HEATING_ZONE = (
        ('Center', '중앙'),
        ('Division', '개별'),
        ('Area', '지역'),
    )
    title = models.CharField(max_length=20, verbose_name='제목', )
    description = models.TextField(max_length=1000, verbose_name='설명', )
    address = models.OneToOneField(
        'PostAddress',
        on_delete=models.CASCADE,
    )
    salesForm = models.OneToOneField(
        'SalesForm',
        on_delete=models.CASCADE,
    )

    floor = models.IntegerField(null=True, verbose_name='층 수', )
    totalFloor = models.IntegerField(null=True, verbose_name='건물 층 수', )
    area = models.IntegerField(verbose_name='전용 면적', )
    supplyArea = models.IntegerField(verbose_name='공급 면적', )
    shortRent = models.BooleanField()
    management = models.ManyToManyField(
        'ControlPoint',
        through='MaintenanceFee',
    )
    parkingFee = models.IntegerField(verbose_name='주차 비용', null=True)
    moveIn = models.DateTimeField(verbose_name='입주 가능 날짜')
    option = models.ManyToManyField('OptionItem', verbose_name='옵션 항목')
    heatingType = models.CharField('난방 종류', choices=HEATING_ZONE, max_length=10)
    pet = models.BooleanField('반려 동물', )
    elevator = models.BooleanField('엘레베이터', )
    multiFloor = models.BooleanField('복층', )
    pointRoom = models.BooleanField('1.5 룸, 주방 분리형')
    builtIn = models.BooleanField('빌트 인', )
    veranda = models.BooleanField('베란다/발코니', )
    depositLoan = models.BooleanField('전세 자금 대출', )
    securitySafety = models.ManyToManyField(
        'SecuritySafetyFacilities',
    )


class PostAddress(models.Model):
    loadAddress = models.CharField(max_length=50, )


class SalesForm(models.Model):
    type = models.CharField(max_length=10)
    deposit = models.IntegerField(null=True, verbose_name='보증금', )  # 보증금
    monthly = models.IntegerField(null=True, verbose_name='월세', )  # 월세
    salePrice = models.IntegerField(null=True, verbose_name='매매 가격', )  # 매매가격

    @staticmethod
    def start():
        type_list = ['매매', '전세', '월세']
        for i in type_list:
            SalesForm.objects.create(
                type=i,
            )


class MaintenanceFee(models.Model):
    postRoom = models.ForeignKey(PostRoom, verbose_name='해당 매물', on_delete=models.CASCADE, )
    controlPoint = models.ForeignKey('ControlPoint', verbose_name='포함 항목', on_delete=models.CASCADE, )
    totalFee = models.IntegerField(verbose_name='관리비 합계')


# 관리비 포함 항목
class ControlPoint(models.Model):
    name = models.CharField(max_length=10, verbose_name='포함 항목 물품')


class OptionItem(models.Model):
    name = models.CharField('옵션 항목 아이템', max_length=10)
    image = models.ImageField('옵션 이미지', null=True, )


class SecuritySafetyFacilities(models.Model):
    name = models.CharField('보안/안전 시설 아이템', max_length=10, )
    image = models.ImageField('시설 이미지', null=True, )


class PostLike(models.Model):
    post = models.ForeignKey(PostRoom, on_delete=models.CASCADE, )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True, )
