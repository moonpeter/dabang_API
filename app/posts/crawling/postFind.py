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
        # 'https://www.dabangapp.com/room/5e42b371a11d530866144078',
        # 'https://www.dabangapp.com/room/5e1d6b0773d078168238f1e0',
        # 'https://www.dabangapp.com/room/5e1548a8de8c7b54c2c917dc',
        # 'https://www.dabangapp.com/room/5e914f0dc38c0c4ce5a8318c',
        'https://www.dabangapp.com/room/5e8d35bd0cf5a5412d6da2ea',
        'https://www.dabangapp.com/room/5e914cb3cc41dc1f46a7b6c3',
        'https://www.dabangapp.com/room/5e79c60d84be5e7ef8e96461',
        'https://www.dabangapp.com/room/5e914f0455e11d4ce5fbd245',
        'https://www.dabangapp.com/room/5e8e7cf99d891c3904c57951',
        'https://www.dabangapp.com/room/5e6c6cced93974472c59c6b8',
        'https://www.dabangapp.com/room/5e8aa7fcffe08e36cb56b4ce',
        'https://www.dabangapp.com/room/5e746c5855cade1ff3b2c900',
        'https://www.dabangapp.com/room/5e72c8819888397a3638a424',
        'https://www.dabangapp.com/room/5e8c62242dca726fb8181a93',
        'https://www.dabangapp.com/room/5e7bfd7b290cb26ec37087b2',
        'https://www.dabangapp.com/room/5e8d248ea8c2115d1680b1ce',
        'https://www.dabangapp.com/room/5e819e0e2ce1b126d9c88027',
        'https://www.dabangapp.com/room/5e7ad2422247205b43406c05',
        'https://www.dabangapp.com/room/5e8ae5dd2a140b19ad1152a0',
        'https://www.dabangapp.com/room/5e9166c6243bed3a047b44c7',
        'https://www.dabangapp.com/room/5e7ad24a5809285b43dd6156',
        'https://www.dabangapp.com/room/5e783d0a32767735792361c6',
        'https://www.dabangapp.com/room/5e8acea9ce4f3e4ec40793d4',
        'https://www.dabangapp.com/room/5e7c13ee116bff1a5c1b0fe5',
        'https://www.dabangapp.com/room/5e7ecdf238420950529b2564',
        'https://www.dabangapp.com/room/5e9172a37c5daf1246d1e0b8',
        'https://www.dabangapp.com/room/5e7c7166244673686b638419',
        'https://www.dabangapp.com/room/5e6b164652c2753d337b4179',
        'https://www.dabangapp.com/room/5e8aa4778e97eb10a32212da',
        'https://www.dabangapp.com/room/5e7c36033dc51b7e45ba7b1f',
        'https://www.dabangapp.com/room/5e8ea6167f954b7088471d4c',
        'https://www.dabangapp.com/room/5e7c52fea861501550e7e8a3',
        'https://www.dabangapp.com/room/5e90026d91315870a836a8b2',
        'https://www.dabangapp.com/room/5e72ec87fdf308458942257f',
        'https://www.dabangapp.com/room/5e7307f8017a955b71279100',
        'https://www.dabangapp.com/room/5e7ac6c2cbf0df08eb1d61ff',
        'https://www.dabangapp.com/room/5e71ab6ddeb6c10f9e935e0a',
        'https://www.dabangapp.com/room/5e7efa460358215304f057de',
        'https://www.dabangapp.com/room/5e756335964ed823fc81e0f8',
        'https://www.dabangapp.com/room/5e7c2481a50ed345f63c82d2',
        'https://www.dabangapp.com/room/5e7ec95111e1011a7ec7e203',
        'https://www.dabangapp.com/room/5e81a1b829cfcc06f34d07af',
        'https://www.dabangapp.com/room/5e8eab2db72bfe784f349eb9',
        'https://www.dabangapp.com/room/5e72e2cf83e008062fb55d61',
        'https://www.dabangapp.com/room/5e868a4369367f4ba04cbd9a',
        'https://www.dabangapp.com/room/5e819d03b701a426d98a42ea',
        'https://www.dabangapp.com/room/5e914f0ba6d8364ce5f7703e',
        'https://www.dabangapp.com/room/5e72ea274f0cc61c30fd8f36',
        'https://www.dabangapp.com/room/5e71de843a4ea4174fa94faa',
        'https://www.dabangapp.com/room/5e916938513ff8418a568eed',
        'https://www.dabangapp.com/room/5e8d3248d7b3d87429517725',
        'https://www.dabangapp.com/room/5e8ac8522eccde46164a92d3',
        'https://www.dabangapp.com/room/5e7acbcb77c7d1101fafdd2f',
        'https://www.dabangapp.com/room/5e6f1211e8174c468ae971a6',
        'https://www.dabangapp.com/room/5e7ae6cdfccb516fda9bd67a',
        'https://www.dabangapp.com/room/5e6f0a419f0dec7f7c305a0f',
        'https://www.dabangapp.com/room/5e72c4a3811444445417df08',
        'https://www.dabangapp.com/room/5e83f3eaee50375db934125d',
        'https://www.dabangapp.com/room/5e8d636cdc19e6397ec46d1e',
        'https://www.dabangapp.com/room/5e8ac3f8d5f8af65d9d3516d',
        'https://www.dabangapp.com/room/5e81beab3da96b3251ddf7eb',
        'https://www.dabangapp.com/room/5e8fed22182fb750ac3ed90c',
        'https://www.dabangapp.com/room/5e81aed624e07a1c823c3867',
        'https://www.dabangapp.com/room/5e9161db119d0812848e85f6',
        'https://www.dabangapp.com/room/5e8a9c86b3222941bb9d625c',
        'https://www.dabangapp.com/room/5e7c7162b2dfed686b7f24ed',
        'https://www.dabangapp.com/room/5e7afd8e99ef8a59f3a5afd9',
        'https://www.dabangapp.com/room/5e7c715f773e22686b15ee5c',
        'https://www.dabangapp.com/room/5e8aaa98521b226396ccdbbf',
        'https://www.dabangapp.com/room/5e9001ff37e57c46f8c99f48',
        'https://www.dabangapp.com/room/5e8be7742fa6cd03e13c708b',
        'https://www.dabangapp.com/room/5e9006e3bf780d2cb29e8d0f',
        'https://www.dabangapp.com/room/5e8293bb31c88476954f7213',
        'https://www.dabangapp.com/room/5e8bddbea4736e4e7859a818',
        'https://www.dabangapp.com/room/5e914f1527b8e84ce5955ba0',
        'https://www.dabangapp.com/room/5e9151a6dfdeb4412ec75483',
        'https://www.dabangapp.com/room/5e919ebcf6898d237c673810',
        'https://www.dabangapp.com/room/5e916e0e2398e0656787dea5',
        'https://www.dabangapp.com/room/5e7ae6101b845266b335b028',
        'https://www.dabangapp.com/room/5e8ab2a116fdf52419a4663e',
        'https://www.dabangapp.com/room/5e82935402a1f77695464902',
        'https://www.dabangapp.com/room/5e91707f35f33d6d89aed70a',
        'https://www.dabangapp.com/room/5e8ae5d9ff822c19ad4d0911',
        'https://www.dabangapp.com/room/5e8d213f2e87de0bdd660b28',
        'https://www.dabangapp.com/room/5e7c1d58c603891137e21986',
        'https://www.dabangapp.com/room/5e8bdd0323820f30a80c8b75',
        'https://www.dabangapp.com/room/5e8d689d895f204256bc67c5',
        'https://www.dabangapp.com/room/5e8e7a0bb2d08c242d00ef0e',
        'https://www.dabangapp.com/room/5e6f433852da4f5e153acde8',
        'https://www.dabangapp.com/room/5e71aec6af6ef63ffd56a238',
        'https://www.dabangapp.com/room/5e71ab25234ea90f9e3684a6',
        'https://www.dabangapp.com/room/5e857bc1b4e0795b8a572512',
        'https://www.dabangapp.com/room/5e8ec761980d512302d88076',
        'https://www.dabangapp.com/room/5e8812ec29ec2d636a1d92ca',
        'https://www.dabangapp.com/room/5e6f0f71bcde1c6b698fdc41',
        'https://www.dabangapp.com/room/5e84665fdec4512c8b64192a',
        'https://www.dabangapp.com/room/5e914cb88bd3631f46a09e81',
        'https://www.dabangapp.com/room/5e6f0ca8c990b036c43197c1',
        'https://www.dabangapp.com/room/5e70ab27caeda435adaadb1f',
        'https://www.dabangapp.com/room/5e71a7797741213bb1749b0d',
        'https://www.dabangapp.com/room/5e75868ff87c48462892dcd0',
        'https://www.dabangapp.com/room/5e9151a226ca77412e85f0b4',
        'https://www.dabangapp.com/room/5e9001d9004a6b46f8e283bc',
        'https://www.dabangapp.com/room/5e8812e4b1d930636a6d8e56',
        'https://www.dabangapp.com/room/5e8d77eec22836604787ccb7',
        'https://www.dabangapp.com/room/5e8ac6d37f0d924616315449',
        'https://www.dabangapp.com/room/5e916e46b360f06567cedb09',
        'https://www.dabangapp.com/room/5e71de3ebd9532174f661894',
        'https://www.dabangapp.com/room/5e7b21cb77efb279fa89895b',
        'https://www.dabangapp.com/room/5e7c1ff47c26285ff0f5b216',
        'https://www.dabangapp.com/room/5e901025f3ff9d77d2ee73f7',
        'https://www.dabangapp.com/room/5e8bd952c5710167918ef972',
        'https://www.dabangapp.com/room/5e7c30a8febb732852667dc1',
        'https://www.dabangapp.com/room/5e8fe7146ee1804a3f82a6c4',
        'https://www.dabangapp.com/room/5e70733be64ca9665e5a9759',
        'https://www.dabangapp.com/room/5e8e87131a056b7de982d60c',
        'https://www.dabangapp.com/room/5e8ab2d3e5b96224197411d8',
        'https://www.dabangapp.com/room/5e6f33247c85125a56950333',
        'https://www.dabangapp.com/room/5e9168ebfd958b418a717e6a',
        'https://www.dabangapp.com/room/5e818950279b951d62cb4760',
        'https://www.dabangapp.com/room/5e71959aa3f116628a7b5917',
        'https://www.dabangapp.com/room/5e7026c96db9eb6cbda862e9',
        'https://www.dabangapp.com/room/5e917082011fd86d896240c1',
        'https://www.dabangapp.com/room/5e6f0bf4aa08bd36c473df19',
        'https://www.dabangapp.com/room/5e7c1d79e58bcf11370fb44e',
        'https://www.dabangapp.com/room/5e8c2e7efbefce1fe5167abd',
        'https://www.dabangapp.com/room/5e819de582c86726d99a8ee5',
        'https://www.dabangapp.com/room/5e7c323bccafa13d5abd89ba',
        'https://www.dabangapp.com/room/5e8ead5550fe9507241a4fb6',
        'https://www.dabangapp.com/room/5e8ff5dc57abf65d42b86d86',
        'https://www.dabangapp.com/room/5e8ab40e3d0b3003b99b42f7',
        'https://www.dabangapp.com/room/5e900e32810cf44966ac6385',
        'https://www.dabangapp.com/room/5e6ae2e92f0a64540a1f6be7',
        'https://www.dabangapp.com/room/5e7431f250356c4b2e118c0c',
        'https://www.dabangapp.com/room/5e85790803871a2aa7b0afdb',
        'https://www.dabangapp.com/room/5e900e1e00708f49663fd402',
        'https://www.dabangapp.com/room/5e8edff144048f63141f001c',
        'https://www.dabangapp.com/room/5e9146a83fb2521b2c49ecee',
        'https://www.dabangapp.com/room/5e6b431f9dbf8b2583721312',
        'https://www.dabangapp.com/room/5e86f4b7e302b11c09fae313',
        'https://www.dabangapp.com/room/5e7ae14bc6b15433d28cf62f',
        'https://www.dabangapp.com/room/5e86a3c6c3bafd57a1dd6a77',
        'https://www.dabangapp.com/room/5e8e8645245cf677356da8aa',
        'https://www.dabangapp.com/room/5e7068cae8747815b23d81e4',
        'https://www.dabangapp.com/room/5e8ae5ed851dda19ad8b717d',
        'https://www.dabangapp.com/room/5e8154e74cd9607c21f9d10c',
        'https://www.dabangapp.com/room/5e8aac2b54de271a14e4c32e',
        'https://www.dabangapp.com/room/5e856698c18a88387dfe7d10',
        'https://www.dabangapp.com/room/5e814fd64039fb0ab049a6d8',
        'https://www.dabangapp.com/room/5e8d6e4dd2170c747784db4e',
        'https://www.dabangapp.com/room/5e8a945fee38c71dd70b0cb0',
        'https://www.dabangapp.com/room/5e82b23608fecc73e61f4d63',
        'https://www.dabangapp.com/room/5e7d6469c88b2e4d3edf63ab',
        'https://www.dabangapp.com/room/5e7ed445b9ca165a0abe5c37',
        'https://www.dabangapp.com/room/5e81884c1e326a0478fe722b',
        'https://www.dabangapp.com/room/5e7c0280a77db85208d4fc64',
        'https://www.dabangapp.com/room/5e82d5bb15e93834534e5f52',
        'https://www.dabangapp.com/room/5e7c3a23c85f5376a60e8fc9',
        'https://www.dabangapp.com/room/5e8c1f6ef9ae1d50cbdf754b',
        'https://www.dabangapp.com/room/5e82b22081a85e73e67a5dda',
        'https://www.dabangapp.com/room/5e7ac451a96dd2389c19493c',
        'https://www.dabangapp.com/room/5e8812e58751ff636a485f05',
        'https://www.dabangapp.com/room/5e8550aabea97b7a22578734',
        'https://www.dabangapp.com/room/5e8830b78321b32902cade76',
        'https://www.dabangapp.com/room/5e81610280554a6b432242ca',
        'https://www.dabangapp.com/room/5e8e76abab03dd31e56dcb71',
        'https://www.dabangapp.com/room/5e7d692a742312505a5190d4',
        'https://www.dabangapp.com/room/5e79ac00e7b2ac67af850dcf',
        'https://www.dabangapp.com/room/5e61eb268c45fb4368c1a174',
        'https://www.dabangapp.com/room/5dea1592bfd6ae3b8ca406ce',
        'https://www.dabangapp.com/room/5e6f0321aeeb591276221de3',
        'https://www.dabangapp.com/room/5e8c3d4a27ee572fb48cf07d',
        'https://www.dabangapp.com/room/5e9034ed4ef6ae3420ccbfb7',
        'https://www.dabangapp.com/room/5e81a2cd918a981d67c29e72',
        'https://www.dabangapp.com/room/5e82f884d770ee57c7f381cf',
        'https://www.dabangapp.com/room/5d64b386c2523c16a42f3d07',
        'https://www.dabangapp.com/room/5e71d3578c6d8b3b99af9f05',
        'https://www.dabangapp.com/room/5e1e71f971ee814758fbcdc3',
        'https://www.dabangapp.com/room/5df1eb02d5887d7930797275',
        'https://www.dabangapp.com/room/5d9c54de54340c1c977f92d8',
        'https://www.dabangapp.com/room/5e4a2310faa1647355958b95',
        'https://www.dabangapp.com/room/5e4a1c16cc7257682001c153',
        'https://www.dabangapp.com/room/579704dc6f1b3a094aec5f57',
        'https://www.dabangapp.com/room/5e71af111d650303159f0348',
        'https://www.dabangapp.com/room/5e4a2ece3982731d6e5b52d7',
        'https://www.dabangapp.com/room/5e58feb4bab02104722d161f',
        'https://www.dabangapp.com/room/5e4643a33e033020a5e53f8d',
        'https://www.dabangapp.com/room/5df1ea294eac3d7bfabcba03',
        'https://www.dabangapp.com/room/5e72fa154944a63dbd73fe69',
        'https://www.dabangapp.com/room/5e60b25b0cf47a0ed2719309',
        'https://www.dabangapp.com/room/5e72c6b3f4b5b86fe3c8f385',
        'https://www.dabangapp.com/room/5e33edce22c6252a97b9a7d0',
        'https://www.dabangapp.com/room/5e7047cb6896ee286b243867',
        'https://www.dabangapp.com/room/5e86edc1914a1d1d7ef51ac2',
        'https://www.dabangapp.com/room/5e84034e55c6882f23bd690e',
        'https://www.dabangapp.com/room/5e843dc1031dc142631601df',
        'https://www.dabangapp.com/room/5b0e2eea5ed74c7355786247',
        'https://www.dabangapp.com/room/5e3befe9e242632ffa06bc85',
        'https://www.dabangapp.com/room/5e72be16b85b0e6fc9a7a7cc',
        'https://www.dabangapp.com/room/5e8f01b3cec5d415e90d4cf6',
        'https://www.dabangapp.com/room/5e82ffe2f112a16b1126ca5e',
        'https://www.dabangapp.com/room/5e572e5757f09c5638273c20',
        'https://www.dabangapp.com/room/5d9ec99fc9a3dd4b29e3efcd',
        'https://www.dabangapp.com/room/5d8ee7ac7fa17e2f2267239a',
        'https://www.dabangapp.com/room/5e843a4d99a00c17e3bc85c4',
        'https://www.dabangapp.com/room/5813063a2e6f462359315117',
        'https://www.dabangapp.com/room/5e8591a5880dfc22b9e0970f',
        'https://www.dabangapp.com/room/5dd4f8a12bda4e34e57d0447',
        'https://www.dabangapp.com/room/5e6759cdb979bc71e9afeab2',
        'https://www.dabangapp.com/room/5e0f3718d96bea310291e09a',
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
        if '※' in address:
            print('주소값이 이상하게 들어감')
            address = driver.find_element_by_xpath('/html/body/div[1]/div/div[5]/div[4]/div/p')
            address = address.get_attribute('innerText')
        print(address)
        address_ins, __ = PostAddress.objects.get_or_create(
            loadAddress=address,
        )
        print(address_ins)

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
