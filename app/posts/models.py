from django.db import models
from config import settings


class PostRoom(models.Model):
    HEATING_ZONE = (
        ('Center', '중앙'),
        ('Division', '개별'),
        ('Area', '지역'),
    )
    title = models.CharField(max_length=20, verbose_name='제목', null=True, )
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
    living_expenses = models.CharField('생활비', null=True, max_length=15, )
    living_expenses_detail = models.CharField('생활비 항목', null=True, max_length=20, )
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

    @staticmethod
    def crawling():
        from selenium import webdriver
        from selenium.common.exceptions import NoSuchElementException
        import collections

        dabang_url = 'https://www.dabangapp.com/search#/map?filters=%7B%22multi_room_type%22%3A%5B2%2C1%2C0%5' \
                     'D%2C%22selling_type%22%3A%5B0%2C1%2C2%5D%2C%22deposit_range%22%3A%5B0%2C999999%5D%2C%22price' \
                     '_range%22%3A%5B0%2C999999%5D%2C%22trade_range%22%3A%5B0%2C999999%5D%2C%22maintenance_cost_rang' \
                     'e%22%3A%5B0%2C999999%5D%2C%22include_maintenance_option1%22%3Atrue%2C%22room_size%22%3A%5B0' \
                     '%2C999999%5D%2C%22supply_space_range%22%3A%5B0%2C999999%5D%2C%22room_floor_multi%22%3A%5B1%2C2' \
                     '%2C3%2C4%2C7%2C6%2C5%5D%2C%22division%22%3Afalse%2C%22duplex%22%3Afalse%2C%22room_' \
                     'type%22%3A%5B1%2C2%5D%2C%22enter_date_range%22%3A%5B0%2C999999%5D%2C%22parking_avera' \
                     'ge_range%22%3A%5B0%2C999999%5D%2C%22household_num_range%22%3A%5B0%2C999999%5D%2C%22park' \
                     'ing%22%3Afalse%2C%22animal%22%3Afalse%2C%22short_lease%22%3Afalse%2C%22full_option%22%3Af' \
                     'alse%2C%22built_in%22%3Afalse%2C%22elevator%22%3Afalse%2C%22balcony%22%3Afalse%2C%22loan%22' \
                     '%3Afalse%2C%22safety%22%3Afalse%2C%22pano%22%3Afalse%2C%22deal_type%22%3A%5B0%2C1%5D%7D&po' \
                     'sition=%7B%22location%22%3A%5B%5B127.03782637531295%2C37.518247186167436%5D%2C%5B127.0778725' \
                     '3873349%2C37.56435875152705%5D%5D%2C%22center%22%3A%5B127.05784328891325%2C37.541304716670695%' \
                     '5D%2C%22zoom%22%3A6%7D&search=%7B%22id%22%3A%2211200114%22%2C%22type%22%3A%22region%22%2C%22nam' \
                     'e%22%3A%22%EC%84%B1%EC%88%98%EB%8F%991%EA%B0%80%22%7D&tab=all'
        driver = webdriver.Chrome('/Users/mac/projects/ChromeWebDriver/chromedriver')
        driver.implicitly_wait(3)

        driver.get(dabang_url)
        seongsoo_1dong_detail_list = driver.find_elements_by_xpath(
            "/html/body/div[1]/div/div[2]/div[1]/div/div[2]/ul/li/div/a")
        seongsoo_1dong_detail_list[0].get_attribute("href")
        bang_url_list = []

        [bang_url_list.append(url.get_attribute('href')) for url in seongsoo_1dong_detail_list]

        # 각 게시글 조회 시작
        for url in bang_url_list:
            driver.get(url)
            driver.implicitly_wait(3)

            try:
                driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/div/button").click()
            except NoSuchElementException:
                pass

            variable = collections.namedtuple('variable', ['description', 'address', 'salesForm', 'floor',
                                                           'totalFloor', 'area', 'supplyArea', 'shortRent',
                                                           'management', 'parkingFee', 'living_expenses',
                                                           'living_expenses_detail', 'moveIn', 'option',
                                                           'heatingType', 'pet', 'elevator', 'multiFloor',
                                                           'pointRoom', 'builtIn', 'veranda', 'depositLoan',
                                                           'securitySafety',
                                                           ])

            unrefined_securitySafety = driver.find_elements_by_xpath('/html/body/div[1]/div/div[5]/div[3]/div[2]/div')
            security = unrefined_securitySafety[0].get_attribute('innerText')
            security = security.split('\n\n')
            # security MTM

            try:
                unrefined_option = driver.find_elements_by_xpath('/html/body/div[1]/div/div[5]/div[3]/div[1]/div')
            except NoSuchElementException:
                pass
            unrefined_option = unrefined_option[0].get_attribute('innerText')
            unrefined_option = unrefined_option.split('\n\n')
            option = unrefined_option
            # option은 옵션테이블 MTM

            unrefined_description = driver.find_elements_by_xpath("/html/body/div[1]/div/div[4]/div/div")
            unrefined_description[0].get_attribute("innerText")
            variable.description = unrefined_description.replace("\n", "")

            unrefined_address = driver.find_elements_by_xpath('/html/body/div[1]/div/div[5]/div/div/p')
            variable.address = unrefined_address[0].get_attribute("innerText")

            unrefined_salesform = driver.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div/ul/li[1]/div')
            salesForm = unrefined_salesform[0].get_attribute("innerText")
            salesForm = salesForm.replace('/', ' ')
            salesForm = salesForm.replace('\n', '')
            salesForm = salesForm.split()

            # SalesForm OTO relation
            variable.salesForm_type = salesForm[0]
            variable.salesForm_deposit = salesForm[1]
            variable.salesForm_monthly = salesForm[2]

            unrefined_floor = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[1]/div')
            total_floor = unrefined_floor[0].get_attribute('innerText')
            total_floor = total_floor.split('/')
            floor = total_floor[0]
            variable.floor = floor
            totalFloor = total_floor[1]
            totalFloor = totalFloor.replace(' ', '')
            variable.totalFloor = totalFloor

            unrefined_area = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[2]/div/span')
            area = unrefined_area[0].get_attribute('innerText')
            variable.area = area
            driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[2]/div/button').click()
            unrefined_area = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[2]/div/span')
            supplyArea = unrefined_area[0].get_attribute('innerText')
            variable.supplyArea = supplyArea

            unrefined_shortRent = driver.find_elements_by_xpath(
                '/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[5]/p')
            shortRent = unrefined_shortRent[0].get_attribute('innerText')
            variable.shortRent = shortRent

            if shortRent == '불가능':
                variable.shortRent = False
            else:
                variable.shortRent = True

            unrefined_management = driver.find_elements_by_xpath(
                '/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[3]')
            unrefined_management = unrefined_management[0].get_attribute('innerText')
            unrefined_management = unrefined_management.replace('\n', '')
            unrefined_management = unrefined_management.replace(' ', '')
            unrefined_management = unrefined_management.replace('(', ' ')
            unrefined_management = unrefined_management.replace(')', ' ')
            unrefined_management = unrefined_management.replace(',', ' ')
            unrefined_management = unrefined_management.split(' ')
            # 관리비 금액
            management = unrefined_management.pop(0)
            totalPay = management.split('만')
            detailPay = totalPay[0]
            # 관리비 인스턴스로 생성
            # detailPay는 MaintenanceFee의 totalFee로

            try:
                unrefined_living_expenses = driver.find_elements_by_xpath(
                    '/html/body/div[1]/div/div[5]/div[2]/div/div/div/label')
                unrefined_living_expenses_detail = driver.find_elements_by_xpath(
                    '/html/body/div[1]/div/div[5]/div[2]/div/div/div/span')
            except NoSuchElementException:
                pass
            unrefined_living_expenses = unrefined_living_expenses[0].get_attribute('innerText')
            living_expenses = unrefined_living_expenses.replace(' ', '')
            variable.living_expenses = living_expenses
            living_expenses_detail = unrefined_living_expenses_detail[0].get_attribute('innerText')
            variable.living_expenses_detail = living_expenses_detail

            unrefined_parking = driver.find_elements_by_xpath(
                "/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[4]/p")
            parking = unrefined_parking[0].get_attribute('innerText')
            variable.parkingFee = parking

            unrefined_moveIn = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[9]/div')
            moveIn = unrefined_moveIn[0].get_attribute('innerText')
            variable.moveIn = moveIn

            unrefined_heatingType = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[3]/div')
            heatingType = unrefined_heatingType[0].get_attribute('innerText')
            variable.heatingType = heatingType

            unrefined_pet = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[6]/div')
            pet = unrefined_pet[0].get_attribute('innerText')
            variable.pet = pet

            unfined_elevator = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[5]/div')
            elevator = unfined_elevator[0].get_attribute('innerText')
            variable.elevator = elevator

            unrefined_builtIn = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[4]/div')
            builtIn = unrefined_builtIn[0].get_attribute('innerText')
            variable.builtIn = builtIn

            unrefined_veranda = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[7]/div')
            veranda = unrefined_veranda[0].get_attribute('innerText')
            variable.veranda = veranda

            unrefined_depositLoan = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[8]/div')
            depositLoan = unrefined_depositLoan[0].get_attribute('innerText')
            variable.depositLoan = depositLoan

            # 주소 인스턴스 생성
            address_instance = PostAddress.objects.create(
                loadAddress=variable.address
            )
            # 판매 유형 인스턴스 생
            salesform = SalesForm.objects.get_or_create(
                type=variable.salesForm_type,
                deposit=variable.salesForm_deposit,
                monthly=variable.salesForm_monthly,
            )

            # 관리비 인스턴스 생성 MTM
            management_list = []
            for obj in management:
                if not obj == '':
                    instance = ControlPoint.objects.get_or_create(name=obj)
                else:
                    pass
                management_list.append(instance)

            # 안전 시설 인스턴스 생성 MTM
            security_list = []
            for obj in security:
                instance = SecuritySafetyFacilities.objects.create(
                    name=obj,
                )
                security_list.append(instance)

            # 옵션 시설 인스턴스 생성 MTM
            option_list = []
            for obj in option:
                instance = OptionItem.objects.create(
                    name=obj,
                )
                option_list.append(instance)

            # objects create
            post = PostRoom.objects.create(
                description=variable.description,
                address=address_instance,
                salesForm=salesform,
                floor=variable.floor,
                totalfloor=variable.totalFloor,
                area=variable.area,
                supplyArea=variable.supplyArea,
                shortRent=variable.shortRent,
                living_expenses=variable.living_expenses,
                living_expenses_detail=variable.living_expenses_detail,
                parkingFee=variable.parkingFee,
                moveIn=variable.moveIn,
                heatingType=variable.heatingType,
                pet=variable.pet,
                elevator=variable.elevator,
                builtIn=variable.builtIn,
                veranda=variable.veranda,
                depositLoan=variable.depositLoan,
            )

            # 관리비 항목 관계 정립
            controlPoint = ControlPoint.objects.get(name=obj)
            maintenance = MaintenanceFee.objects.create(
                postRoom=post,
                controlPoint=controlPoint,
                totalFee=detailPay,
            )
            for obj in management_list[1:]:
                maintenance.controlPoint.add(obj)

            for obj in security_list:
                post.securitySafety.add(obj)

            for obj in option_list:
                post.option.add(obj)


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
