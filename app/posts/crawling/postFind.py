import os
import re
import time
import urllib

from django.core.files import File
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from config.settings import MEDIA_ROOT
from posts.crawling.find_urls import find_apartment_urls, find_urls
from ..models import SalesForm, PostAddress, SecuritySafetyFacilities, OptionItem, \
    MaintenanceFee, RoomOption, RoomSecurity, PostRoom, Broker, PostImage, AdministrativeDetail
from bs4 import BeautifulSoup


def postFind():
    driver = webdriver.Chrome('/Users/mac/projects/ChromeWebDriver/chromedriver')
    # driver = webdriver.Chrome('/Users/moonpeter/Desktop/Selenium/chromedriver')

    # 다방 성수동 매물 url
    # url_all_list = find_apartment_urls()
    # url_all_list += find_urls()
    # print('url_all_list len >>', type(url_all_list), '\n')
    # print('url_all_list >>', url_all_list, '\n')
    url_all_list = [
                    'https://www.dabangapp.com/room/5e33bb027bfab713de85a774',
                    'https://www.dabangapp.com/room/5e72bf479c854870aa02c352',
                    'https://www.dabangapp.com/room/5e6b586d27e43b013e9ba597',
                    'https://www.dabangapp.com/room/5e3845a2d7447c3fabc904e3',
                    'https://www.dabangapp.com/room/5dede10eeea3c95b23de6927',
                    'https://www.dabangapp.com/room/5e86a6ebd985b83a8fa2a24e',
                    'https://www.dabangapp.com/room/5e9193985526841afcfe4133',
                    'https://www.dabangapp.com/room/5e4b99581a00fb457ff0ef63',
                    'https://www.dabangapp.com/room/5e816497deec6b3194f63705',
                    'https://www.dabangapp.com/room/5e9192b1afa34c2320474d61',
                    'https://www.dabangapp.com/room/5cbea76d71e887479063ac59',
                    'https://www.dabangapp.com/room/5e8ace5e7702c43897f858ac',
                    'https://www.dabangapp.com/room/5d652a2654311c3fa94d6ee2',
                    'https://www.dabangapp.com/room/5d9af15512468a5ee4605669',
                    'https://www.dabangapp.com/room/5e8ea363d86a754325dcc5ae',
                    'https://www.dabangapp.com/room/5e91566b0f96861e75b1b60f',
                    'https://www.dabangapp.com/room/5e2f8a15fd3dc349995a75d7',
                    'https://www.dabangapp.com/room/5d1aaaf7f8675e2ee22fd097',
                    'https://www.dabangapp.com/room/5ddd53a496557639e70c825e',
                    'https://www.dabangapp.com/room/5e4cc48194bb1c050fceb147',
                    'https://www.dabangapp.com/room/5d89b7deb3be6628c11e79d4',
                    'https://www.dabangapp.com/room/5da19747bf668c3e1d36d1af',
                    'https://www.dabangapp.com/room/5e4ceabfac08d4432ca2e889',
                    'https://www.dabangapp.com/room/5e7997c5619be26de13760d1',
                    'https://www.dabangapp.com/room/5e8581abf11589776af13eac',
                    'https://www.dabangapp.com/room/5e19204fd1e8ba59c8b5d7f4',
                    'https://www.dabangapp.com/room/5df9e1954c971122317f86f2',
                    'https://www.dabangapp.com/room/5e7c52a336e37e1fa669f93e',
                    'https://www.dabangapp.com/room/5e8c077fc6addb21400412cb',
                    'https://www.dabangapp.com/room/5e4a1a9866bcc56a163dc945',
                    'https://www.dabangapp.com/room/5db78bcdeaa0e9359de71c0f',
                    'https://www.dabangapp.com/room/5e5f7d649d2d5f4a00a465af',
                    'https://www.dabangapp.com/room/5e3cfc049d81167ed198e975',
                    'https://www.dabangapp.com/room/5e60b894ea6fdf19bd4dd16b',
                    'https://www.dabangapp.com/room/581ae8a8f7f1fe26fd7d65f0',
                    'https://www.dabangapp.com/room/5b442f6802c75b70610826a9',
                    'https://www.dabangapp.com/room/5d652a2654311c3fa94d6ee2',
                    'https://www.dabangapp.com/room/5d9af15512468a5ee4605669',
                    'https://www.dabangapp.com/room/5e8ea363d86a754325dcc5ae',
                    'https://www.dabangapp.com/room/5e91566b0f96861e75b1b60f',
                    'https://www.dabangapp.com/room/5e2f8a15fd3dc349995a75d7',
                    'https://www.dabangapp.com/room/5d1aaaf7f8675e2ee22fd097',
                    'https://www.dabangapp.com/room/5ddd53a496557639e70c825e',
                    'https://www.dabangapp.com/room/5e4cc48194bb1c050fceb147',
                    'https://www.dabangapp.com/room/5d89b7deb3be6628c11e79d4',
                    'https://www.dabangapp.com/room/5da19747bf668c3e1d36d1af',
                    'https://www.dabangapp.com/room/5e4ceabfac08d4432ca2e889',
                    'https://www.dabangapp.com/room/5e7997c5619be26de13760d1',
                    'https://www.dabangapp.com/room/5e8581abf11589776af13eac',
                    'https://www.dabangapp.com/room/5e19204fd1e8ba59c8b5d7f4',
                    'https://www.dabangapp.com/room/5df9e1954c971122317f86f2',
                    'https://www.dabangapp.com/room/5e7c52a336e37e1fa669f93e',
                    'https://www.dabangapp.com/room/5e8c077fc6addb21400412cb',
                    'https://www.dabangapp.com/room/5e4a1a9866bcc56a163dc945',
                    'https://www.dabangapp.com/room/5db78bcdeaa0e9359de71c0f',
                    'https://www.dabangapp.com/room/5e5f7d649d2d5f4a00a465af',
                    'https://www.dabangapp.com/room/5e3cfc049d81167ed198e975',
                    'https://www.dabangapp.com/room/5e60b894ea6fdf19bd4dd16b',
                    'https://www.dabangapp.com/room/581ae8a8f7f1fe26fd7d65f0',
                    'https://www.dabangapp.com/room/5b442f6802c75b70610826a9',
                    'https://www.dabangapp.com/room/5e577d972d69ed5194f1eefa',
                    'https://www.dabangapp.com/room/5e268a6db427ae304ec68e3f',
                    'https://www.dabangapp.com/room/582fb3c519e7cb55ecce2534',
                    'https://www.dabangapp.com/room/5e659c74f2a3ac415c367599',
                    'https://www.dabangapp.com/room/5e6343c4869f5c579367bd0c',
                    'https://www.dabangapp.com/room/5e84996da1218276a29e79cc',
                    'https://www.dabangapp.com/room/5e83fbfaa2b0597ae67aaf10',
                    'https://www.dabangapp.com/room/5e89aadd49dee06a434e251e',
                    'https://www.dabangapp.com/room/5e47792095a5332028d312b8',
                    'https://www.dabangapp.com/room/5e8d36c5643ef26fe5d7a23a',
                    'https://www.dabangapp.com/room/5df9d39d26a54f7ee4cd126d',
                    'https://www.dabangapp.com/room/5c0e5ccffc1a300f6fbeedaa',
                    'https://www.dabangapp.com/room/5e477835ee4ea021e01ba0af',
                    'https://www.dabangapp.com/room/5e8bed42a6a79a728f5ac21d',
                    'https://www.dabangapp.com/room/5df05b64849a606d56f017e9',
                    'https://www.dabangapp.com/room/5e3bdb7635fc9778dae9d35a',
                    'https://www.dabangapp.com/room/5e843414848c0b61944e50c5',
                    'https://www.dabangapp.com/room/5d07c75b3742fe7603630b43',
                    'https://www.dabangapp.com/room/5e7c21ceab438338a1b79479',
                    'https://www.dabangapp.com/room/5c5d8557e98ed333425a3cb4',
                    'https://www.dabangapp.com/room/59f3e67dc6cda31e4c4f8b33',
                    'https://www.dabangapp.com/room/5e69d334d3ac974a856143f1'
                    ]

    # 각 게시글 조회 시작
    for post_index, url in enumerate(url_all_list):
        driver.get(url)
        time.sleep(2)

        # 중개인
        # Broker
        try:
            button = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/ul/li/button")
            driver.execute_script("arguments[0].click();", button)

            name = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[1]/div[1]/h1')
            name = name.get_attribute('innerText')

            address = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[1]/div[1]/p')
            address = address.get_attribute('innerText')

            manager = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[2]/div[2]/p[1]')
            manager = manager.get_attribute('innerText')

            tel = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[2]/div[2]/p[2]')
            tel = tel.get_attribute('innerText')
        except NoSuchElementException:
            manager = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/p[1]')
            manager = manager.get_attribute('innerText')

            tel = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/p[2]')
            tel = tel.get_attribute('innerText')
        button = driver.find_element_by_xpath("/html/body/div[4]/div/div/header/button")
        driver.execute_script("arguments[0].click();", button)

        broker_ins = Broker.objects.get_or_create(
            name=name,
            address=address,
            manager=manager,
            tel=tel,
        )
        # 상세 설명 보기
        try:
            button = driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/div/button")
            driver.execute_script("arguments[0].click();", button)
        except NoSuchElementException:
            pass

        # 매물 형태
        time.sleep(2)
        post_type = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/ul/li[1]/p/span')
        post_type = post_type.get_attribute('innerText')

        # 방 정보 설명
        description = driver.find_elements_by_xpath("/html/body/div[1]/div/div[4]/div/div")
        description = description[0].get_attribute("innerText")
        description.replace("\n", "")

        # 매물 형식
        unrefined_salesform = driver.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div/ul/li[1]/div')
        salesForm = unrefined_salesform[0].get_attribute("innerText")
        salesForm = salesForm.replace('/', ' ')
        salesForm = salesForm.replace('\n', '')
        salesForm = salesForm.split()
        salesType = salesForm[0]  # sales type

        salesDepositChar = salesForm[1]
        if salesDepositChar.find('원'):
            salesDepositChar = salesDepositChar.replace('원', '')

        salesdepositInt = salesDepositChar.replace('억', '00000000')
        if salesdepositInt.find('만'):
            salesdepositInt = salesdepositInt.replace('만', '')
        salesdepositInt = int(salesdepositInt)

        try:
            salesmonthlyChar = salesForm[2]

            salesmonthlyInt = salesmonthlyChar.replace('만원', '0000')
            salesmonthlyInt = int(salesmonthlyInt)

            if salesType == '전세':
                # 전세는 금액이 억, 만원이 붙어 있는 경우가 있어서 이렇게 처리.
                salesdepositInt = salesdepositInt + salesmonthlyInt
                salesDepositChar = salesDepositChar + salesmonthlyChar
        except IndexError:
            salesmonthlyInt = 0
            salesmonthlyChar = ''

        salesform_ins = SalesForm.objects.create(
            type=salesType,
            depositChar=salesDepositChar,
            monthlyChar=salesmonthlyChar,
            depositInt=salesdepositInt,
            monthlyInt=salesmonthlyInt,
        )

        if post_type == "아파트":
            if salesType == "매매":
                address = driver.find_elements_by_xpath('/html/body/div[1]/div/div[5]/div[3]/div/p')
            else:
                address = driver.find_elements_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div/p')
        else:
            address = driver.find_elements_by_xpath('/html/body/div[1]/div/div[5]/div[4]/div/p')
        if not address:
            address = driver.find_elements_by_xpath('/html/body/div[1]/div/div[5]/div/div/p')

        address = address[0].get_attribute('innerText')

        address_ins = PostAddress.objects.create(
            loadAddress=address
        )

        unrefined_floor = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[1]/div')
        total_floor = unrefined_floor[0].get_attribute('innerText')
        total_floor = total_floor.split('/')
        floor = total_floor[0]

        totalFloor = total_floor[1]
        totalFloor = totalFloor.replace(' ', '')

        areaChar = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[2]/div/span')
        areaChar = areaChar[0].get_attribute('innerText')

        # 평수로 변환하는 버
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[2]/div/button').click()

        unrefined_area = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[2]/div/span')
        supplyAreaChar = unrefined_area[0].get_attribute('innerText')

        supplyAreaInt = supplyAreaChar.split('/')
        supplyAreaInt = supplyAreaInt[1].replace('평', '')

        supplyAreaInt = supplyAreaInt.strip()

        supplyAreaInt = int(supplyAreaInt)

        try:
            if post_type == '아파트':
                unrefined_shortRent = driver.find_elements_by_xpath(
                    '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[5]/p')
            else:
                unrefined_shortRent = driver.find_elements_by_xpath(
                    '/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[5]/p')
                if not unrefined_shortRent:
                    unrefined_shortRent = driver.find_elements_by_xpath(
                        '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[4]/p')
            shortRent = unrefined_shortRent[0].get_attribute('innerText')
            shortRent = shortRent

            if shortRent == '불가능':
                shortRent = False
            else:
                shortRent = True

        except IndexError:
            # 매매에서는 단기임대가 없음.
            shortRent = None

        # 관리비 클래스
        try:
            if post_type == "아파트":
                management = driver.find_element_by_xpath(
                    '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[3]')
            else:
                if salesType == "매매":
                    management = driver.find_element_by_xpath(
                        '/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[2]')
                else:
                    management = driver.find_element_by_xpath(
                        '/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[3]')
        except NoSuchElementException:
            management = None

        try:
            management = management.get_attribute('innerText')
            management = management.replace('\n', '')
            management = management.replace(' ', '')
            management = management.replace('(', ' ')
            management = management.replace(')', ' ')
            management = management.replace(',', ' ')
            management = management.strip(' ')
            management = management.split(' ')

        except AttributeError:
            pass

        try:
            managementPay = management.pop(0)
            if managementPay.find('만원'):
                managementPay = managementPay.replace('만원', ' ')
                if managementPay == '없음':
                    managementPay = 0
                elif managementPay == '문의':
                    managementPay = 0
                managementPay = float(managementPay)
            else:
                managementPay = 0
            totalFee = managementPay

        except IndexError:
            pass
        except AttributeError:
            pass
        except NameError:
            pass

        # 관리비 마무리

        try:
            if post_type == "아파트":
                if salesType == "매매":
                    unrefined_parking = None
                else:
                    unrefined_parking = driver.find_elements_by_xpath(
                        '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[4]/p')

            else:
                if salesType == "매매":
                    # 일반 주택 매매
                    try:
                        unrefined_parking = driver.find_elements_by_xpath(
                            "/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[3]")
                    except IndexError:
                        unrefined_parking = driver.find_elements_by_xpath(
                            '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[3]/p')
                else:
                    unrefined_parking = driver.find_elements_by_xpath(
                        "/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[4]/p")
            parkingDetail = unrefined_parking[0].get_attribute('innerText')
        except IndexError:
            unrefined_parking = driver.find_elements_by_xpath(
                '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[4]/p'
            )
            parkingDetail = unrefined_parking[0].get_attribute('innerText')
        except TypeError:
            parkingDetail = '불가'

        if parkingDetail == '불가':
            parkingTF = False
        else:
            parkingTF = True

        try:
            if not salesType == "매매":
                if post_type == "아파트":
                    unrefined_living_expenses = driver.find_elements_by_xpath(
                        '/html/body/div[1]/div/div[5]/div[3]/div/div/div/label')
                    unrefined_living_expenses_detail = driver.find_elements_by_xpath(
                        '/html/body/div[1]/div/div[5]/div[3]/div/div/div/span')
                else:
                    try:
                        unrefined_living_expenses = driver.find_elements_by_xpath(
                            '/html/body/div[1]/div/div[5]/div[2]/div/div/div/label')
                        unrefined_living_expenses_detail = driver.find_elements_by_xpath(
                            '/html/body/div[1]/div/div[5]/div[2]/div/div/div/span')
                    except NoSuchElementException:
                        unrefined_living_expenses = driver.find_elements_by_xpath(
                            '/html/body/div[1]/div/div[5]/div[3]/div/div/div/label')
                        unrefined_living_expenses_detail = driver.find_elements_by_xpath(
                            '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[3]/p[2]/span')
            else:
                living_expenses = None
                living_expenses_detail = None
        except NoSuchElementException:
            pass

        # 생활비 , 생활비 항목들
        try:
            unrefined_living_expenses = unrefined_living_expenses[0].get_attribute('innerText')
            living_expenses = unrefined_living_expenses.replace(' ', '')
            living_expenses_detail = unrefined_living_expenses_detail[0].get_attribute('innerText')

        except IndexError:
            unrefined_living_expenses = driver.find_elements_by_xpath(
                '/html/body/div[1]/div/div[5]/div[3]/div/div/div/label'
            )
            unrefined_living_expenses_detail = driver.find_elements_by_xpath(
                '/html/body/div[1]/div/div[5]/div[3]/div/div/div/span')
            unrefined_living_expenses = unrefined_living_expenses[0].get_attribute('innerText')
            living_expenses = unrefined_living_expenses.replace(' ', '')
            living_expenses_detail = unrefined_living_expenses_detail[0].get_attribute('innerText')
        except TypeError:
            print('생활비 항목 타입 에러')
        except NameError:
            print('생활비 항목 이름 에러')
        except AttributeError:
            print(unrefined_living_expenses, "가 없")

        if salesType == "매매":
            if post_type == "아파트":
                moveIn = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[7]/div')
            else:
                moveIn = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[7]/div')
        else:
            if post_type == "아파트":
                moveIn = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[9]/div')
            else:
                moveIn = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[9]/div')
        MoveInChar = moveIn.get_attribute('innerText')
        # option & sceurity

        try:
            option_tag = driver.find_element_by_name('option')
            option_tag = option_tag.get_attribute('innerText')
            option_tag = option_tag.split('보안/안전시설')
            print('option tag >> ', option_tag)
            option = option_tag[0]
            option = option.split('\n\n')
            print(option)
            del option[0]
            del option[-1]
            print(option)

            print('result option', option)

            security = option_tag[1]
            security = security.split('\n\n')
            del security[-1]
            del security[0]
            print('result security', security)
        except IndexError:
            print('안전 시설 없음.')
            security = None
        except NoSuchElementException:
            print('옵션, 안전시설 없음', url)
            option = None
            security = None

        # Room option instance create
        if option is not None:
            option_list = []
            POSTS_IMAGE_DIR = os.path.join(MEDIA_ROOT, f'.posts/.option/')
            for option_name in option:
                f = open(os.path.join(POSTS_IMAGE_DIR, f'{option_name}.png'), 'rb')
                ins = OptionItem.objects.get_or_create(
                    name=option_name,
                    image=File(f),
                )
                f.close()

                option_list.append(ins[0])

        # Security option instance create
        if security is not None:
            POSTS_IMAGE_DIR = os.path.join(MEDIA_ROOT, f'.posts/.security/')
            security_list = []
            print('안전 시설은 ', security)

            for security_name in security:
                f = open(os.path.join(POSTS_IMAGE_DIR, f'{security_name}.png'), 'rb')
                ins = SecuritySafetyFacilities.objects.get_or_create(
                    name=security_name,
                    image=File(f),
                )
                f.close()

                security_list.append(ins[0])
                print('security >>>', ins[0])

        heatingType = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[3]/div')
        heatingType = heatingType.get_attribute('innerText')

        if salesType == "매매":
            if post_type == "아파트":
                pet = True
            else:
                pet = True
        else:
            if post_type == "아파트":
                pet = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[7]/div')
            else:
                pet = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[6]/div')
            pet = pet.get_attribute('innerText')
            if pet == "불가능":
                pet = False
            else:
                pet = True

        if post_type == "아파트":
            elevator = True
        else:
            elevator = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[5]/div')
            elevator = elevator.get_attribute('innerText')
            if elevator == "있음":
                elevator = True
            else:
                elevator = False

        if post_type == "아파트":
            builtIn = True
        else:
            builtIn = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[4]/div')
            builtIn = builtIn.get_attribute('innerText')
            if builtIn == "아님":
                builtIn = False
            else:
                builtIn = True
        # 베란다
        if post_type == "아파트":
            veranda = True
        else:
            if salesType == '매매':
                veranda = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[6]/div')
                veranda = veranda.get_attribute('innerText')
                if veranda == "있음":
                    veranda = True
                else:
                    veranda = False
            else:
                veranda = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[7]/div')
                veranda = veranda.get_attribute('innerText')
                if veranda == '있음':
                    veranda = True
                else:
                    veranda = False
        # depositLoan 전세 대출 자금
        if post_type == '아파트':
            if salesType == '매매':
                depositLoan = True
            else:
                depositLoan = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[8]/div')
                depositLoan = depositLoan.get_attribute('innerText')
                if depositLoan == '가능':
                    depositLoan = True
                else:
                    depositLoan = False
        else:
            if salesType == '매매':
                depositLoan = True
            else:
                depositLoan = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[8]/div')
                depositLoan = depositLoan.get_attribute('innerText')
                if depositLoan == '가능':
                    depositLoan = True
                else:
                    depositLoan = False

        # totalCitizen
        if post_type == '아파트':
            totalCitizen = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[5]/div')
            totalCitizen = totalCitizen.get_attribute('innerText')
        else:
            totalCitizen = None

        if post_type == "아파트":
            totalPark = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[6]/div')
            totalPark = totalPark.get_attribute('innerText')
        else:
            totalPark = None

        if post_type == "아파트":
            totalPark = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[6]/div')
            totalPark = totalPark.get_attribute('innerText')
        else:
            totalPark = None

        # 준공 완료일
        if post_type == '아파트':
            complete = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[4]/div')
            complete = complete.get_attribute('innerText')
        else:
            complete = None

        post = PostRoom.objects.get_or_create(
            broker=broker_ins[0],
            type=post_type,
            description=description,
            address=address_ins,
            salesForm=salesform_ins,
            floor=floor,
            totalFloor=totalFloor,
            areaChar=areaChar,
            supplyAreaChar=supplyAreaChar,
            supplyAreaInt=supplyAreaInt,
            shortRent=shortRent,
            parkingDetail=parkingDetail,
            parkingTF=parkingTF,
            living_expenses=living_expenses,
            living_expenses_detail=living_expenses_detail,
            MoveInChar=MoveInChar,
            heatingType=heatingType,
            pet=pet,
            elevator=elevator,
            builtIn=builtIn,
            veranda=veranda,
            depositLoan=depositLoan,
            totalCitizen=totalCitizen,
            totalPark=totalPark,
            complete=complete,
        )
        if management is not None:
            admin_instance_list = []
            for obj in management:
                admin_ins = AdministrativeDetail.objects.get_or_create(
                    name=obj,
                )
                admin_instance_list.append(admin_ins[0])
        else:
            admin_instance_list = None

        if admin_instance_list is not None:
            for ins in admin_instance_list:
                print('admin_instance_list : ins >>', ins)
                MaintenanceFee.objects.create(
                    postRoom=post[0],
                    totalFee=totalFee,
                    admin=ins,
                )

        if option is not None:
            for ins in option_list:
                RoomOption.objects.create(
                    postRoom=post[0],
                    option=ins,

                )
                print(ins)
        if security is not None:
            for ins in security_list:
                RoomSecurity.objects.create(
                    postRoom=post[0],
                    security=ins,

                )

        div_list = driver.find_elements_by_xpath('/html/body/div[1]/div/div[3]/div/div[2]/div')

        image_list = []

        for i, url in enumerate(div_list):
            cls_name = url.get_attribute('class')
            cls_name = cls_name.split(' ')
            cls_name = cls_name[1]
            photo = driver.execute_script(
                f'return window.getComputedStyle(document.querySelector(".{cls_name}"),":after").getPropertyValue("background")')

            test_url = re.findall(r'"(.*?)"', photo)

            # 이미지 파일이 아닌 url를 뺀 새로운 url list
            if test_url:
                if 'dabang' in test_url[0]:
                    pass
                else:
                    image_list.append(test_url[0])
            else:
                print('빈 리스트')

        POSTS_DIR = os.path.join(MEDIA_ROOT, '.posts')

        if not os.path.exists(POSTS_DIR):
            os.makedirs(POSTS_DIR, exist_ok=True)

        if image_list:
            for index, image_url in enumerate(image_list):
                print('image_url>> ', image_url)
                try:
                    POSTS_IMAGE_DIR = os.path.join(MEDIA_ROOT, f'.posts/{post[0].pk}/')
                    if not os.path.exists(POSTS_IMAGE_DIR):
                        os.makedirs(POSTS_IMAGE_DIR, exist_ok=True)

                    # 이미지 생성
                    image_save_name = os.path.join(POSTS_IMAGE_DIR, f'{index}.jpg')
                    urllib.request.urlretrieve(image_url, image_save_name)
                    f = open(os.path.join(POSTS_IMAGE_DIR, f'{index}.jpg'), 'rb')
                    PostImage.objects.get_or_create(
                        image=File(f),
                        post=post[0],
                    )
                    f.close()
                except FileExistsError:
                    print('이미 존재하는 파일')

        # print('이미지 업로드 끝')
        print('게시글 하나 크롤링 완성 pk:', post_index)
    driver.close()
