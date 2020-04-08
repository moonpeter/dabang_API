from django.db import models

from config import settings
from posts.crawling.find_urls import find_apartment_urls


class PostRoom(models.Model):
    broker = models.ForeignKey(
        'posts.Broker',
        on_delete=models.SET_NULL,
        null=True,
    )
    HEATING_ZONE = (
        ('Center', '중앙'),
        ('Division', '개별'),
        ('Area', '지역'),
    )
    type = models.CharField('매물 종류', max_length=10, null=True, )
    description = models.TextField(max_length=200, verbose_name='설명', )
    address = models.OneToOneField(
        'posts.PostAddress',
        on_delete=models.CASCADE,
    )
    salesForm = models.OneToOneField(
        'posts.SalesForm',
        on_delete=models.CASCADE,
    )
    floor = models.CharField(null=True, verbose_name='층 수', max_length=5)
    totalFloor = models.CharField(null=True, verbose_name='건물 층 수', max_length=5)
    areaInt = models.IntegerField(verbose_name='정수형 전용 면적', null=True, )
    areaChar = models.CharField(verbose_name='문자형 전용 면적', max_length=10, null=True, )
    supplyAreaInt = models.IntegerField(verbose_name='정수형 공급 면적', )
    supplyAreaChar = models.CharField(verbose_name='문자형 공급 면적', max_length=10, null=True, )
    # areaInt는 api로 작성 시 필요, areaChar 는 크롤링 부분에서 사용. area까진 정수로 변경해주지 않는다. 필터링에서 사용하지 않기 때문
    # supplyArea는 api에서 사용 , supplyArea char는 크롤링에서 사용, 필터링에 사용하므로 int형으로 변환
    # 공급면적을 기준으로 변환한다.
    shortRent = models.BooleanField(null=True, )
    management = models.ManyToManyField(
        'posts.AdministrativeDetail',
        through='MaintenanceFee',
    )
    parkingDetail = models.CharField(verbose_name='주차 비용', null=True, max_length=10)
    parkingTF = models.BooleanField('주차 가능 유무')
    living_expenses = models.CharField('생활비', null=True, max_length=15, )
    living_expenses_detail = models.CharField('생활비 항목', null=True, max_length=20, )

    MoveInChar = models.CharField('크롤링용 입주날짜', null=True, max_length=10)
    moveInDate = models.DateTimeField(verbose_name='입주 가능 날짜', null=True, )
    option = models.ManyToManyField('OptionItem', through='RoomOption', verbose_name='옵션 항목')
    heatingType = models.CharField('난방 종류', max_length=10)
    # choice field 쓰는게 지금 좀 애매해서 되나 제가 따로 해볼게요
    pet = models.BooleanField('반려 동물', )
    elevator = models.BooleanField('엘레베이터', )
    multiFloor = models.BooleanField('복층', null=True, )
    pointRoom = models.BooleanField('1.5 룸, 주방 분리형', null=True, )
    builtIn = models.BooleanField('빌트 인', null=True, )
    veranda = models.BooleanField('베란다/발코니', null=True, )
    depositLoan = models.BooleanField('전세 자금 대출', null=True, )
    totalCitizen = models.CharField('총 세대 수', max_length=10, null=True, )
    parkingAccumulation = models.CharField('세대당 주차 대수', max_length=10, null=True, )
    complete = models.CharField('준공 년 월', max_length=10, null=True, )
    securitySafety = models.ManyToManyField(
        'posts.SecuritySafetyFacilities',
        through='RoomSecurity',

    )

    @staticmethod
    def project_crawling_start():
        from posts.crawling.postFind import postFind
        post_type = input('아파트면 아파트 입력, 아니면 그냥 엔터')
        postFind(post_type)


class PostAddress(models.Model):
    loadAddress = models.CharField(max_length=50, )
    detailAddress = models.CharField(max_length=30, null=True, )


class SalesForm(models.Model):
    # 우선 크롤링 코드 되는지만 확인 이후 인티저로 바꿀건데 그건 좀 생각하고 짜야 할
    type = models.CharField(max_length=10, verbose_name='매물 종류', )
    depositChar = models.CharField(null=True, verbose_name='문자형 매매-보증금', max_length=10)  # 보증금
    monthlyChar = models.CharField(null=True, verbose_name='문자형 월세', max_length=10)  # 월세
    depositInt = models.IntegerField('정수형 매매-보증금', null=True, )
    monthlyInt = models.IntegerField('정수형 월세', null=True, )

    @staticmethod
    def start():
        type_list = ['매매', '전세', '월세']
        for i in type_list:
            SalesForm.objects.create(
                type=i,
            )


class MaintenanceFee(models.Model):
    postRoom = models.ForeignKey('posts.PostRoom', verbose_name='해당 매물', on_delete=models.CASCADE, )
    admin = models.ForeignKey('posts.AdministrativeDetail', verbose_name='포함 항목', on_delete=models.CASCADE, )
    totalFee = models.IntegerField(verbose_name='관리비 합계')


# 관리비 포함 항목
class AdministrativeDetail(models.Model):
    name = models.CharField(max_length=10, verbose_name='포함 항목 물품')


class OptionItem(models.Model):
    name = models.CharField('옵션 항목 아이템', max_length=10)
    image = models.ImageField('옵션 이미지', null=True, )


class SecuritySafetyFacilities(models.Model):
    name = models.CharField('보안/안전 시설 아이템', max_length=10, )
    image = models.ImageField('시설 이미지', null=True, )


class PostLike(models.Model):
    post = models.ForeignKey('posts.PostRoom', on_delete=models.CASCADE, )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True, )


class RoomOption(models.Model):
    postRoom = models.ForeignKey('posts.PostRoom', verbose_name='해당 매물', on_delete=models.CASCADE, )
    option = models.ForeignKey(OptionItem, verbose_name='해당 옵션', on_delete=models.CASCADE, )
    created_at = models.DateTimeField(auto_now_add=True, )


class RoomSecurity(models.Model):
    postRoom = models.ForeignKey('posts.PostRoom', verbose_name='해당 매물', on_delete=models.CASCADE, )
    security = models.ForeignKey('posts.SecuritySafetyFacilities', verbose_name='보안 안전 시설', on_delete=models.CASCADE, )
    created_at = models.DateTimeField(auto_now_add=True, )


class Broker(models.Model):
    name = models.CharField('회사 명', max_length=30, null=True, )
    address = models.CharField('주소', max_length=20, null=True, )
    manager = models.CharField('중개인', max_length=10, null=True, )
    tel = models.CharField('전화번호', max_length=13, null=True, )
