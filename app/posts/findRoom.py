# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# import collections
# import time
#
# from .models import SalesForm, PostAddress, AdministrativeDetail, SecuritySafetyFacilities, OptionItem, \
#     MaintenanceFee, PostRoom
#
#
# def findRoom():
#     dabang_url = 'https://www.dabangapp.com/search#/map?filters=%7B%22multi_room_type%22%3A%5B2%2C1%2C0%5' \
#                  'D%2C%22selling_type%22%3A%5B0%2C1%2C2%5D%2C%22deposit_range%22%3A%5B0%2C999999%5D%2C%22price' \
#                  '_range%22%3A%5B0%2C999999%5D%2C%22trade_range%22%3A%5B0%2C999999%5D%2C%22maintenance_cost_rang' \
#                  'e%22%3A%5B0%2C999999%5D%2C%22include_maintenance_option1%22%3Atrue%2C%22room_size%22%3A%5B0' \
#                  '%2C999999%5D%2C%22supply_space_range%22%3A%5B0%2C999999%5D%2C%22room_floor_multi%22%3A%5B1%2C2' \
#                  '%2C3%2C4%2C7%2C6%2C5%5D%2C%22division%22%3Afalse%2C%22duplex%22%3Afalse%2C%22room_' \
#                  'type%22%3A%5B1%2C2%5D%2C%22enter_date_range%22%3A%5B0%2C999999%5D%2C%22parking_avera' \
#                  'ge_range%22%3A%5B0%2C999999%5D%2C%22household_num_range%22%3A%5B0%2C999999%5D%2C%22park' \
#                  'ing%22%3Afalse%2C%22animal%22%3Afalse%2C%22short_lease%22%3Afalse%2C%22full_option%22%3Af' \
#                  'alse%2C%22built_in%22%3Afalse%2C%22elevator%22%3Afalse%2C%22balcony%22%3Afalse%2C%22loan%22' \
#                  '%3Afalse%2C%22safety%22%3Afalse%2C%22pano%22%3Afalse%2C%22deal_type%22%3A%5B0%2C1%5D%7D&po' \
#                  'sition=%7B%22location%22%3A%5B%5B127.03782637531295%2C37.518247186167436%5D%2C%5B127.0778725' \
#                  '3873349%2C37.56435875152705%5D%5D%2C%22center%22%3A%5B127.05784328891325%2C37.541304716670695%' \
#                  '5D%2C%22zoom%22%3A6%7D&search=%7B%22id%22%3A%2211200114%22%2C%22type%22%3A%22region%22%2C%22nam' \
#                  'e%22%3A%22%EC%84%B1%EC%88%98%EB%8F%991%EA%B0%80%22%7D&tab=all'
#     driver = webdriver.Chrome('/Users/mac/projects/ChromeWebDriver/chromedriver')
#
#     driver.get(dabang_url)
#     seongsoo_1dong_detail_list = driver.find_elements_by_xpath(
#         "/html/body/div[1]/div/div[2]/div[1]/div/div[2]/ul/li/div/a")
#     seongsoo_1dong_detail_list[0].get_attribute("href")
#     bang_url_list = []
#
#     [bang_url_list.append(url.get_attribute('href')) for url in seongsoo_1dong_detail_list]
#
#     # 각 게시글 조회 시작
#     for url in bang_url_list:
#         driver.get(url)
#         driver.implicitly_wait(3)
#         time.sleep(3)
#
#         try:
#             button = driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/div/button")
#             driver.execute_script("arguments[0].click();", button)
#         except NoSuchElementException:
#             pass
#
#         variable = collections.namedtuple('variable', [
#             'description',
#             # address OTO
#             'addressLoad',
#             # sales Form OTO
#             'salesType',
#             'salesDepositChar',
#             'salesmonthlyChar',
#             'salesdepositInt',
#             'salesmonthlyInt',
#
#             'floor',
#             'totalFloor',
#             'areaChar',
#             'supplyArea',
#             'supplyAreaChar',
#             'supplyAreaInt',
#             'shortRent',
#
#             'living_expenses',
#             'living_expenses_detail',
#             'parkingTF',
#             'parkingDetail',
#
#             'MoveInChar',
#             'heatingType',
#             'pet',
#             'elevator',
#             'builtIn',
#             'veranda',
#             'depositLoan',
#         ])
#         unrefined_description = driver.find_elements_by_xpath("/html/body/div[1]/div/div[4]/div/div")
#         description = unrefined_description[0].get_attribute("innerText")
#         description.replace("\n", "")
#
#         unrefined_address = driver.find_elements_by_xpath('/html/body/div[1]/div/div[5]/div/div/p')
#         variable.addressLoad = unrefined_address[0].get_attribute("innerText")
#
#         unrefined_salesform = driver.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div/ul/li[1]/div')
#         variable.salesForm = unrefined_salesform[0].get_attribute("innerText")
#         variable.salesForm = variable.salesForm.replace('/', ' ')
#         variable.salesForm = variable.salesForm.replace('\n', '')
#         variable.salesForm = variable.salesForm.split()
#         variable.salesType = variable.salesForm[0]  # sales type
#         variable.salesDepositChar = variable.salesForm[1]
#         if variable.salesDepositChar.find('원'):
#             variable.salesDepositChar = variable.salesDepositChar.replace('원', '')
#         variable.salesdepositInt = variable.salesDepositChar.replace('억', '00000000')
#         variable.salesdepositInt = int(variable.salesdepositInt)
#
#         try:
#             variable.salesmonthlyChar = variable.salesForm[2]
#             variable.salesmonthlyInt = variable.salesmonthlyChar.replace('만원', '0000')
#             variable.salesmonthlyInt = int(variable.salesmonthlyInt)
#             if variable.salesType == '전세':
#                 variable.salesdepositInt = variable.salesdepositInt + variable.salesmonthlyInt
#                 variable.salesDepositChar = variable.salesDepositChar + variable.salesmonthlyChar
#         except IndexError:
#             variable.monthlyChar = variable.salesmonthlyChar,
#
#         salesform = SalesForm.objects.create(
#             type=variable.salesType,
#             depositChar=variable.salesDepositChar,
#             monthlyChar=variable.salesmonthlyChar,
#             depositInt=variable.salesdepositInt,
#             monthlyInt=variable.salesmonthlyInt,
#         )
#
#         unrefined_floor = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[1]/div')
#         total_floor = unrefined_floor[0].get_attribute('innerText')
#         total_floor = total_floor.split('/')
#         floor = total_floor[0]
#         variable.floor = floor
#         totalFloor = total_floor[1]
#         totalFloor = totalFloor.replace(' ', '')
#         variable.totalFloor = totalFloor
#
#         unrefined_area = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[2]/div/span')
#         area = unrefined_area[0].get_attribute('innerText')
#         variable.areaChar = area
#
#         driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[2]/div/button').click()
#
#         unrefined_area = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[2]/div/span')
#         variable.supplyAreaChar = unrefined_area[0].get_attribute('innerText')
#         variable.supplyAreaInt = variable.supplyAreaChar.split('/')
#         variable.supplyAreaInt = variable.supplyAreaInt[1].replace('평', '')
#         variable.supplyAreaInt = variable.supplyAreaInt.strip()
#         variable.supplyAreaInt = int(variable.supplyAreaInt)
#
#         unrefined_shortRent = driver.find_elements_by_xpath(
#             '/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[5]/p')
#         shortRent = unrefined_shortRent[0].get_attribute('innerText')
#         variable.shortRent = shortRent
#
#         if shortRent == '불가능':
#             variable.shortRent = False
#         else:
#             variable.shortRent = True
#
#         unrefined_management = driver.find_elements_by_xpath(
#             '/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[3]')
#         unrefined_management = unrefined_management[0].get_attribute('innerText')
#         unrefined_management = unrefined_management.replace('\n', '')
#         unrefined_management = unrefined_management.replace(' ', '')
#         unrefined_management = unrefined_management.replace('(', ' ')
#         unrefined_management = unrefined_management.replace(')', ' ')
#         unrefined_management = unrefined_management.replace(',', ' ')
#         unrefined_management = unrefined_management.split(' ')
#
#         try:
#             unrefined_living_expenses = driver.find_elements_by_xpath(
#                 '/html/body/div[1]/div/div[5]/div[2]/div/div/div/label')
#             unrefined_living_expenses_detail = driver.find_elements_by_xpath(
#                 '/html/body/div[1]/div/div[5]/div[2]/div/div/div/span')
#         except NoSuchElementException:
#             pass
#
#         unrefined_living_expenses = unrefined_living_expenses[0].get_attribute('innerText')
#         variable.living_expenses = unrefined_living_expenses.replace(' ', '')
#         variable.living_expenses_detail = unrefined_living_expenses_detail[0].get_attribute('innerText')
#
#         unrefined_parking = driver.find_elements_by_xpath(
#             "/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[4]/p")
#         variable.parkingDetail = unrefined_parking[0].get_attribute('innerText')
#         if variable.parkingDetail == '불가':
#             variable.parkingTF = False
#         else:
#             variable.parkingTF = True
#
#         unrefined_moveIn = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[9]/div')
#         variable.MoveInChar = unrefined_moveIn[0].get_attribute('innerText')
#
#         unrefined_heatingType = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[3]/div')
#         heatingType = unrefined_heatingType[0].get_attribute('innerText')
#         variable.heatingType = heatingType
#
#         unrefined_pet = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[6]/div')
#         pet = unrefined_pet[0].get_attribute('innerText')
#         if pet == "불가능":
#             pet = False
#         else:
#             pet = True
#         variable.pet = pet
#
#         unfined_elevator = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[5]/div')
#         elevator = unfined_elevator[0].get_attribute('innerText')
#         if elevator == "없음":
#             elevator = False
#         else:
#             elevator = True
#         variable.elevator = elevator
#
#         unrefined_builtIn = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[4]/div')
#         builtIn = unrefined_builtIn[0].get_attribute('innerText')
#         if builtIn == "아님":
#             builtIn = False
#         else:
#             builtIn = True
#         variable.builtIn = builtIn
#
#         unrefined_veranda = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[7]/div')
#         veranda = unrefined_veranda[0].get_attribute('innerText')
#         if veranda == "없음":
#             veranda = False
#         else:
#             veranda = True
#         variable.veranda = veranda
#
#         unrefined_depositLoan = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[8]/div')
#         depositLoan = unrefined_depositLoan[0].get_attribute('innerText')
#
#         if depositLoan == "가능":
#             depositLoan = True
#         else:
#             depositLoan = False
#         variable.depositLoan = depositLoan
#
#         # 주소 인스턴스 생성
#         address_instance = PostAddress.objects.get_or_create(
#             loadAddress=variable.addressLoad
#         )
#
#         ### 관리비 MTM 관리비 총액, 상세 내역 생성
#         # 관리비 금액
#         managementPay = unrefined_management.pop(0)
#         if managementPay.find('만원'):
#             managementPay = managementPay.replace('만원', ' ')
#             managementPay = int(managementPay)
#         else:
#             managementPay = 0
#         totalFee = managementPay
#
#         # 관리비 디테일
#         admin_list = [item for item in unrefined_management if not item == '']
#         admin_instances = []
#         for ins in admin_list:
#             obj = AdministrativeDetail.objects.get_or_create(name=ins)
#             admin_instances.append(obj)
#
#         # 안전 시설 인스턴스 생성 MTM
#         try:
#             unrefined_securitySafety = driver.find_elements_by_xpath(
#                 '/html/body/div[1]/div/div[5]/div[3]/div[2]/div')
#             security = unrefined_securitySafety[0].get_attribute('innerText')
#             security = security.split('\n\n')
#         # security MTM
#         except IndexError:
#             pass
#         # 안전 시설 obj 생성
#         security_list = []
#         try:
#             for obj in security:
#                 instance = SecuritySafetyFacilities.objects.get_or_create(
#                     name=obj,
#                 )
#                 security_list.append(instance)
#         except UnboundLocalError:
#             pass
#         except NameError:
#             pass
#
#         # option은 옵션테이블 MTM
#         try:
#             unrefined_option = driver.find_elements_by_xpath('/html/body/div[1]/div/div[5]/div[3]/div[1]/div')
#         except NoSuchElementException:
#             pass
#
#         unrefined_option = unrefined_option[0].get_attribute('innerText')
#         unrefined_option = unrefined_option.split('\n\n')
#         option = unrefined_option
#         option_ins_list = []
#         for ins in option:
#             option_ins_list.append(ins)
#
#         # 옵션 시설 인스턴스 생성 MTM
#         option_list = []
#         for obj in option:
#             instance = OptionItem.objects.create(
#                 name=obj,
#             )
#             option_list.append(instance)
#
#         # objects create
#
#         post = PostRoom.objects.get_or_create(
#             description=variable.description,
#             address=address_instance[0],
#             salesForm=salesform,
#             floor=variable.floor,
#             totalFloor=variable.totalFloor,
#             areaChar=variable.areaChar,
#             supplyAreaChar=variable.supplyAreaChar,
#             supplyAreaInt=variable.supplyAreaInt,
#             shortRent=variable.shortRent,
#             living_expenses=variable.living_expenses,
#             living_expenses_detail=variable.living_expenses_detail,
#             parkingDetail=variable.parkingDetail,
#             parkingTF=variable.parkingTF,
#             MoveInChar=variable.MoveInChar,
#             heatingType=variable.heatingType,
#             pet=variable.pet,
#             elevator=variable.elevator,
#             builtIn=variable.builtIn,
#             veranda=variable.veranda,
#             depositLoan=variable.depositLoan,
#         )
#
#         for ins in admin_instances:
#             MaintenanceFee.objects.create(
#                 postRoom=post[0],
#                 totalFee=totalFee,
#                 admin=ins[0],
#             )
