import json
import os
import re
import time
import urllib

import requests
from django.core.files import File
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException

from config import settings
from config.settings import MEDIA_ROOT
from members.models import SocialLogin
from posts.crawling.find_urls import find_apartment_urls, find_urls

from ..models import SalesForm, PostAddress, SecuritySafetyFacilities, OptionItem, \
    MaintenanceFee, RoomOption, RoomSecurity, PostRoom, Broker, PostImage, AdministrativeDetail

KAKAO_APP_ID = settings.KAKAO_APP_ID


def postFind():
    # driver = webdriver.Chrome('/Users/mac/projects/ChromeWebDriver/chromedriver')
    driver = webdriver.Chrome('/Users/moonpeter/Desktop/Selenium/chromedriver')
    SocialLogin.start()
    # 다방 성수동 매물 url
    # url_all_list = find_apartment_urls()
    # print('아파트 단지 url', url_all_list)
    # officetels = find_urls()
    # url_all_list += officetels
    # print('오피스텔 매물', officetels)

    url_all_list = [                    # 오피스텔
                    'https://www.dabangapp.com/room/5e9435995c3ac1609a8fd908',
                    'https://www.dabangapp.com/room/5e82f884d770ee57c7f381cf',
                    'https://www.dabangapp.com/room/5e6759cdb979bc71e9afeab2',
                    'https://www.dabangapp.com/room/5e82ffe2f112a16b1126ca5e',
                    'https://www.dabangapp.com/room/5e93ec571087be6c9d348d9c',
                    'https://www.dabangapp.com/room/5e9fbc3505ff823c392d4d3a',
                    'https://www.dabangapp.com/room/5ea623a3dada043b6e4619b9',
                    'https://www.dabangapp.com/room/5e6f0321aeeb591276221de3',
                    'https://www.dabangapp.com/room/5e9a82fd7329a5563a77274e',
                    'https://www.dabangapp.com/room/5ea0f659ff0f5117661c8408',
                    'https://www.dabangapp.com/room/5e0f3718d96bea310291e09a',
                    'https://www.dabangapp.com/room/5e99601abc1a2e63758d1968',
                    'https://www.dabangapp.com/room/5e9fd19bdea9fc5a7d8f5173',
                    'https://www.dabangapp.com/room/5ea64b9c2ae69e6277fe6169',
                    'https://www.dabangapp.com/room/5e9febd7bf530716fcbf51c5',
                    'https://www.dabangapp.com/room/5e33bb027bfab713de85a774',
                    'https://www.dabangapp.com/room/5e71af111d650303159f0348',
                    'https://www.dabangapp.com/room/5e86edc1914a1d1d7ef51ac2',
                    'https://www.dabangapp.com/room/5e816497deec6b3194f63705',
                    'https://www.dabangapp.com/room/5e9eb0fc7145c11ebb232db9',
                    'https://www.dabangapp.com/room/5d64b386c2523c16a42f3d07',
                    'https://www.dabangapp.com/room/5e967aa03b72e37c4b8e19f4',
                    'https://www.dabangapp.com/room/5e9d038f618ea701e1304f33',
                    'https://www.dabangapp.com/room/5ea64a5363265c685a5f9db0',
                    'https://www.dabangapp.com/room/5df1eb02d5887d7930797275',
                    'https://www.dabangapp.com/room/5ea0f65f7fe6d517660c6615',
                    'https://www.dabangapp.com/room/5e99104de7921f1d798272a3',
                    'https://www.dabangapp.com/room/5ea0f5770eea072ac547b418',
                    'https://www.dabangapp.com/room/5ea0fcfd27599121780b30b1',
                    'https://www.dabangapp.com/room/5e3845a2d7447c3fabc904e3',
                    'https://www.dabangapp.com/room/5ea67f6826769003b4280354',
                    'https://www.dabangapp.com/room/5e58feb4bab02104722d161f',
                    'https://www.dabangapp.com/room/5ea0f58193c1372ac2df539f',
                    'https://www.dabangapp.com/room/5ea3ce6350f429521fa8f957',
                    'https://www.dabangapp.com/room/5e9d03b0eb4f8f27a0b1c0a2',
                    'https://www.dabangapp.com/room/5ea65cbc38e46c2fdc92a4ef',
                    'https://www.dabangapp.com/room/5d9c54de54340c1c977f92d8',
                    'https://www.dabangapp.com/room/5e843a4d99a00c17e3bc85c4',
                    'https://www.dabangapp.com/room/5e992d3359f24d63d2c5afc2',
                    'https://www.dabangapp.com/room/5e84034e55c6882f23bd690e',
                    'https://www.dabangapp.com/room/5e8ace5e7702c43897f858ac',
                    'https://www.dabangapp.com/room/5e97be37ebb9bb57a7d35d5f',
                    'https://www.dabangapp.com/room/5e994fc856dddc1856281d59',
                    'https://www.dabangapp.com/room/5e996a9b7accce730023773e',
                    'https://www.dabangapp.com/room/5e8f01b3cec5d415e90d4cf6',
                    'https://www.dabangapp.com/room/5e4b99581a00fb457ff0ef63',
                    'https://www.dabangapp.com/room/5e870376f429084ca09bcea6',
                    'https://www.dabangapp.com/room/5e9eb9a7db13d21edb07f96e',
                    'https://www.dabangapp.com/room/5d8ee7ac7fa17e2f2267239a',
                    'https://www.dabangapp.com/room/5ea5b918f8f81035004116ce',
                    'https://www.dabangapp.com/room/5df1ea294eac3d7bfabcba03',
                    'https://www.dabangapp.com/room/5e9efb294b187c5a8beb346f',
                    'https://www.dabangapp.com/room/5e9192b1afa34c2320474d61',
                    'https://www.dabangapp.com/room/5e9034ed4ef6ae3420ccbfb7',
                    'https://www.dabangapp.com/room/5ea65cb7aa04a31d3ce76eb4',
                    'https://www.dabangapp.com/room/5ea0f65d8682c517622cd49d',
                    'https://www.dabangapp.com/room/5e94139c0eb4bb3b5f8d29c4',
                    'https://www.dabangapp.com/room/5e89aadd49dee06a434e251e',
                    'https://www.dabangapp.com/room/5e9a69580a6e2a1917b16a4f',
                    'https://www.dabangapp.com/room/5e268a6db427ae304ec68e3f',
                    'https://www.dabangapp.com/room/5e93d057bc9e1620963edf68',
                    'https://www.dabangapp.com/room/5e577d972d69ed5194f1eefa',
                    'https://www.dabangapp.com/room/5db78bcdeaa0e9359de71c0f',
                    'https://www.dabangapp.com/room/5dd3a1f74b94d17fa980f294',
                    'https://www.dabangapp.com/room/5e9d038861e7bf04feff40cc',
                    'https://www.dabangapp.com/room/5e61de5954444f17b12b891d',
                    'https://www.dabangapp.com/room/5e7866f0485b277642a0bea0',
                    'https://www.dabangapp.com/room/5de1e3dcbff13320f9e8c246',
                    'https://www.dabangapp.com/room/5da19747bf668c3e1d36d1af',
                    'https://www.dabangapp.com/room/5ea3d81ed930955fb1abd57f',
                    'https://www.dabangapp.com/room/5c5d8557e98ed333425a3cb4',
                    'https://www.dabangapp.com/room/5e3bd8f8a44600193619046c',
                    'https://www.dabangapp.com/room/5ea64126035662508bc7f862',
                    'https://www.dabangapp.com/room/5e843414848c0b61944e50c5',
                    'https://www.dabangapp.com/room/5e7997c5619be26de13760d1',
                    'https://www.dabangapp.com/room/5ea2a0953031dd62340645b8',
                    'https://www.dabangapp.com/room/5e8d36c5643ef26fe5d7a23a',
                    'https://www.dabangapp.com/room/5ddf97f4224cdd3567cebf9b',
                    'https://www.dabangapp.com/room/5e19204fd1e8ba59c8b5d7f4',
                    'https://www.dabangapp.com/room/5e8e89360988e55bd5c27df0',
                    'https://www.dabangapp.com/room/5ea631e8606e6e51534cb044',
                    'https://www.dabangapp.com/room/5e9d039eedc091134efbe315',
                    'https://www.dabangapp.com/room/5e9a9ccf17b6ea61206f3133',
                    'https://www.dabangapp.com/room/5d1aaaf7f8675e2ee22fd097',
                    'https://www.dabangapp.com/room/5e3bdb7635fc9778dae9d35a',
                    'https://www.dabangapp.com/room/581ae8a8f7f1fe26fd7d65f0',
                    'https://www.dabangapp.com/room/59f3e67dc6cda31e4c4f8b33',
                    'https://www.dabangapp.com/room/5e9c0e2aa154f95c0ef1cd3a',
                    'https://www.dabangapp.com/room/5e9c62555563ac2c0f02f549',
                    'https://www.dabangapp.com/room/5e84996da1218276a29e79cc',
                    'https://www.dabangapp.com/room/5e659c74f2a3ac415c367599',
                    'https://www.dabangapp.com/room/5e92d088e2f8f970339a1816',
                    'https://www.dabangapp.com/room/5e3ba7b9610c7e1f02caba75',
                    'https://www.dabangapp.com/room/5e9960100d9b5158f03c1317',
                    'https://www.dabangapp.com/room/5ddcfaec6e8a987c8a9e65e1',
                    'https://www.dabangapp.com/room/5e8c077fc6addb21400412cb',
                    'https://www.dabangapp.com/room/5ea29c3daeb3b16acd2297d6',
                    'https://www.dabangapp.com/room/5ea11deceb27865ced4c9866',
                    'https://www.dabangapp.com/room/5dc282ff3c2c224b0a79097c',
                    'https://www.dabangapp.com/room/5e958f3d320e1034a235c14c']


    # 각 게시글 조회 시작
    for post_index, url in enumerate(url_all_list):
        print('############################################# 다음 url \n')
        print('url 입니다.', url, '\n')
        driver.get(url)

        time.sleep(2)

        post_type = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/ul/li[1]/p/span')
        post_type = post_type.get_attribute('innerText')

        # 상세 더보기 클릭
        try:
            button = driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div/div/button')
            driver.execute_script("arguments[0].click();", button)
        except NoSuchElementException:
            pass
        # 방 정보 설명
        description = driver.find_elements_by_xpath("/html/body/div[1]/div/div[4]/div/div")
        description = description[0].get_attribute("innerText")
        description.replace("\n", "")
        try:
            if '접기' in description:
                description = description.split('접기')
            description = description[0]
        except IndexError:
            pass

        # 매물 형식
        unrefined_salesform = driver.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div/ul/li[1]/div')
        salesForm = unrefined_salesform[0].get_attribute("innerText")
        salesForm = salesForm.replace('/', ' ')
        salesForm = salesForm.replace('\n', '')
        salesForm = salesForm.split()
        salesType = salesForm[0]  # sales type

        print(salesType)
        print(post_type)
        if salesType == '매매':

            try:
                btn = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/ul/li[3]/button')
                driver.execute_script("arguments[0].click();", btn)

                href = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[1]/a')
                href = href.get_attribute('href')
                print(href)
                driver.get(href)
                time.sleep(1)
                # 중개소 정보 더 보기
                companyName = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[1]/div')
                print(companyName)
                companyName = companyName.get_attribute('innerText')
                print(companyName)

                address = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[8]/div')
                address = address.get_attribute('innerText')
                print(address)
                managerName = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[2]/div')
                managerName = managerName.get_attribute('innerText')
                print(managerName)
                tel = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[3]/div')
                tel = tel.get_attribute('innerText')
                print(tel)
                companyNumber = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[4]/div')
                companyNumber = companyNumber.get_attribute('innerText')
                print(companyNumber)
                brokerage = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[5]/div')
                brokerage = brokerage.get_attribute('innerText')
                print(brokerage)
                dabangCreated_at = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[6]/div')
                dabangCreated_at = dabangCreated_at.get_attribute('innerText')
                print(dabangCreated_at)
                successCount = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[7]/div')
                successCount = successCount.get_attribute('innerText')
                print(successCount)
                image = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div')
                image = image.get_attribute('class')
                image = image.split(' ')
                image = image[1]
                print(image)
                photo = driver.execute_script(
                    f'return window.getComputedStyle(document.querySelector(".{image}"),":after").getPropertyValue("background")')
                print(photo)
                test_url = re.findall(r'"(.*?)"', photo)
                test_url = test_url[0]
                print(test_url)

            except NoSuchElementException:
                managerName = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/p[1]')
                managerName = managerName.get_attribute('innerText')
                if '(' in managerName:
                    managerName = managerName.split('(')
                    managerName = managerName[0]
                tel = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/p[2]')
                tel = tel.get_attribute('innerText')
                if '-' in tel:
                    tel = tel.replace('-', '')
                companyName = None
                address = None
                test_url = None
                companyNumber = None
                brokerage = None
                dabangCreated_at = None
                successCount = None


        else:

            try:
                btn = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/ul/li[4]/button')
                driver.execute_script("arguments[0].click();", btn)

                href = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[1]/a')
                href = href.get_attribute('href')
                print(href)
                driver.get(href)
                time.sleep(1)
                # 중개소 정보 더 보기
                companyName = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[1]/div')
                print(companyName)
                companyName = companyName.get_attribute('innerText')
                print(companyName)

                address = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[8]/div')
                address = address.get_attribute('innerText')
                print(address)
                managerName = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[2]/div')
                managerName = managerName.get_attribute('innerText')
                print(managerName)
                tel = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[3]/div')
                tel = tel.get_attribute('innerText')
                print(tel)
                companyNumber = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[4]/div')
                companyNumber = companyNumber.get_attribute('innerText')
                print(companyNumber)
                brokerage = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[5]/div')
                brokerage = brokerage.get_attribute('innerText')
                print(brokerage)
                dabangCreated_at = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[6]/div')
                dabangCreated_at = dabangCreated_at.get_attribute('innerText')
                print(dabangCreated_at)
                successCount = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/ul/li[7]/div')
                successCount = successCount.get_attribute('innerText')
                print(successCount)
                image = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div')
                image = image.get_attribute('class')
                image = image.split(' ')
                image = image[1]
                print(image)
                photo = driver.execute_script(
                    f'return window.getComputedStyle(document.querySelector(".{image}"),":after").getPropertyValue("background")')
                print(photo)
                test_url = re.findall(r'"(.*?)"', photo)
                test_url = test_url[0]
                print(test_url)

            except NoSuchElementException:
                managerName = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/p[1]')
                managerName = managerName.get_attribute('innerText')
                if '(' in managerName:
                    managerName = managerName.split('(')
                    managerName = managerName[0]
                tel = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/p[2]')
                tel = tel.get_attribute('innerText')
                if '-' in tel:
                    tel = tel.replace('-', '')
                companyName = None
                address = None
                test_url = None
                companyNumber = None
                brokerage = None
                dabangCreated_at = None
                successCount = None
        # button = driver.find_element_by_xpath("/html/body/div[4]/div/div/header/button")
        # driver.execute_script("arguments[0].click();", button)

        broker_ins = Broker.objects.get_or_create(
            companyName=companyName,
            address=address,
            managerName=managerName,
            tel=tel,
            image=test_url,
            companyNumber=companyNumber,
            brokerage=brokerage,
            dabangCreated_at=dabangCreated_at,
            successCount=successCount,
        )
        print(broker_ins)
        # 상세 설명 보기
        driver.get(url)
        print('--')
        try:
            button = driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/div/button")
            driver.execute_script("arguments[0].click();", button)
        except NoSuchElementException:
            pass

        # 매물 형태
        time.sleep(2)
        print('--')
        salesDepositChar = salesForm[1]
        if salesDepositChar.find('원'):
            salesDepositChar = salesDepositChar.replace('원', '')

        salesdepositInt = salesDepositChar.replace('억', '00000000')
        if salesdepositInt.find('만'):
            salesdepositInt = salesdepositInt.replace('만', '')
        salesdepositInt = int(salesdepositInt)

        try:
            salesmonthlyChar = salesForm[2]

            salesmonthlyInt = salesmonthlyChar.replace('만원', '')
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

        try:
            address = address[0].get_attribute('innerText')
            if '※' in address:
                address = driver.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[4]/div/p')

                address = address.get_attribute('innerText')
            print('address >>>>>>>>>>>>', address)
        except NoSuchElementException:
            address = driver.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[5]/div/p')
            address = address.get_attribute('innerText')

        # kakao Local API
        url = f'https://dapi.kakao.com/v2/local/search/address.json?query={address}'
        res = requests.get(url, headers={'Authorization': f'KakaoAK {KAKAO_APP_ID}'})
        str_data = res.text
        json_data = json.loads(str_data)
        lat = json_data['documents'][0]['x']
        lng = json_data['documents'][0]['y']
        print(f'lat, lng >>  {lat} {lng}')
        address_ins, __ = PostAddress.objects.get_or_create(
            loadAddress=address,
        )
        print('address_ins', address_ins)

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

        if post_type == '아파트':
            if salesType == '매매':
                shortRent = False
            else:
                shortRent = driver.find_elements_by_xpath(
                    '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[5]/p')
                shortRent = shortRent[0].get_attribute('innerText')
        else:
            if salesType == '매매':
                shortRent = False
            else:
                shortRent = driver.find_elements_by_xpath(
                    '/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[5]/p')
                if not shortRent:
                    shortRent = driver.find_elements_by_xpath(
                        '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[4]/p')
                shortRent = shortRent[0].get_attribute('innerText')
        print('shortRent is >>', shortRent)

        if shortRent == '불가능':
            shortRent = False
        else:
            shortRent = True

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

        parkingPay = None
        # 주차비 관련
        try:
            if post_type == "아파트":
                if salesType == "매매":
                    parkingDetail = '가능(무료)'
                    parkingTF = True
                else:
                    parkingDetail = driver.find_element_by_xpath(
                        '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[4]/p')
                    parkingDetail = parkingDetail.get_attribute('innerText')
            else:
                if salesType == "매매":
                    try:
                        parkingDetail = driver.find_element_by_xpath(
                            "/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[3]")
                    except NoSuchElementException:
                        parkingDetail = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[3]/p')
                    except IndexError:
                        parkingDetail = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[3]/p')
                    parkingDetail = parkingDetail.get_attribute('innerText')

                else:
                    try:
                        parkingDetail = driver.find_element_by_xpath(
                            "/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[4]/p")
                        parkingDetail = parkingDetail.get_attribute('innerText')
                    except NoSuchElementException:
                        parkingDetail = driver.find_element_by_xpath(
                            '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[4]/p')
                        parkingDetail = parkingDetail.get_attribute('innerText')

        except IndexError:
            unrefined_parking = driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[4]/p'
            )
            parkingDetail = unrefined_parking[0].get_attribute('innerText')

        except TypeError:
            parkingDetail = '불가'
        if '만' in parkingDetail:
            parkingDetail = parkingDetail.split('만')
            parkingDetail = parkingDetail[0]
            parkingPay = float(parkingDetail)
            parkingDetail = '문의'

        # parking Tf
        if parkingDetail == '가능(무료)':
            parkingTF = True
        elif parkingDetail == '문의':
            parkingTF = True
        else:
            parkingTF = False
        print('parking >>>>>>>>>>>>>', parkingDetail, parkingTF, parkingPay)
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
                moveInChar = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[7]/div')
            else:
                moveInChar = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[7]/div')
        else:
            if post_type == "아파트":
                moveInChar = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[9]/div')
            else:
                moveInChar = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[9]/div')

        moveInChar = moveInChar.get_attribute('innerText')
        moveInDate = None
        if '날짜' in moveInChar:
            pass
        elif '즉시' in moveInChar:
            pass
        elif '2' in moveInChar:
            moveInChar = moveInChar.replace('.', '-')
            moveInDate = moveInChar
            moveInChar = '날짜 협의'
        else:
            moveInChar = '날짜 협의'

        print(moveInChar)

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
            # POSTS_IMAGE_DIR = os.path.join(MEDIA_ROOT, f'.posts/.option/')
            for option_name in option:
                # f = open(os.path.join(POSTS_IMAGE_DIR, f'{option_name}.png'), 'rb')
                ins = OptionItem.objects.get_or_create(
                    name=option_name,
                    # image=File(f),
                )
                # f.close()

                option_list.append(ins[0])

        # Security option instance create
        if security is not None:
            # POSTS_IMAGE_DIR = os.path.join(MEDIA_ROOT, f'.posts/.security/')
            security_list = []
            print('안전 시설은 ', security)

            for security_name in security:
                # f = open(os.path.join(POSTS_IMAGE_DIR, f'{security_name}.png'), 'rb')
                ins = SecuritySafetyFacilities.objects.get_or_create(
                    name=security_name,
                    # image=File(f),
                )
                # f.close()

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
            lat=lat,
            lng=lng,
            floor=floor,
            totalFloor=totalFloor,
            areaChar=areaChar,
            supplyAreaChar=supplyAreaChar,
            supplyAreaInt=supplyAreaInt,
            shortRent=shortRent,
            parkingDetail=parkingDetail,
            parkingTF=parkingTF,
            parkingPay=parkingPay,
            living_expenses=living_expenses,
            living_expenses_detail=living_expenses_detail,
            moveInChar=moveInChar,
            moveInDate=moveInDate,
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
        print('게시글 하나 크롤링 완성 pk:', post_index, '-========================================== \n ')

    driver.close()