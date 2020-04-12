# from bs4 import BeautifulSoup
# from selenium import webdriver
# import time
# import requests
#
#
# # url = 'https://www.dabangapp.com/sales-in-lots#/home'
# #
# # options = webdriver.ChromeOptions()
# # options.add_argument('headless') # 웹 브라우저를 뛰우지 않는 옵션 적용
# #
# # driver = webdriver.Chrome('/Users/moonpeter/Desktop/Selenium/chromedriver', options=options)
# # driver.get(url)
# #
# # time.sleep(3)
# #
# # html = driver.page_source
# # soup = BeautifulSoup(html)
# #
# # item = soup.select('.styled__Wrap-sc-19ctn63-0')
# # for i in item:
# #     print("https://www.dabangapp.com" + i.a.attrs['href'])
# #     print(i.select_one('.BuildingName').text)
# #     print(i.select_one('.Address').text)
# #     print(i.select_one('.Header').text)
# #     print(i.select_one('.Price').text)
# #     # print(i.select_one('.Address').text)
# #     # print(i.select_one('.Address').text)
# #     # print(i.select_one('.Address').text)
# #     # print(i.select_one('.Address').text)
# #     # print(i.select_one('.Address').text)
# #     # print(i.select_one('.Address').text)
# #     print()
# # # driver.find_element_by_xpath("")
# #
# #
# # driver.quit()
#
#
# def parse_title():
#     req = requests.get('https://www.dabangapp.com/sales-in-lots#/home')
#     html = req.text
#     soup = BeautifulSoup(html, 'html.parser')
#     my_titles = soup.select(
#         'p'
#         )
#     data = {}
#     for title in my_titles:
#         data[title.text] = title.get('BuildingName')
#     return data