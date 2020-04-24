import os
import re
import time
import urllib

from django.core.files import File
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException

from config.settings import MEDIA_ROOT
from members.models import SocialLogin
from posts.crawling.find_urls import find_apartment_urls, find_urls

from ..models import SalesForm, PostAddress, SecuritySafetyFacilities, OptionItem, \
    MaintenanceFee, RoomOption, RoomSecurity, PostRoom, Broker, PostImage, AdministrativeDetail


def postFind():
    # driver = webdriver.Chrome('/Users/mac/projects/ChromeWebDriver/chromedriver')
    driver = webdriver.Chrome('/Users/moonpeter/Desktop/Selenium/chromedriver')
    SocialLogin.start()
    # 다방 성수동 매물 url
    # url_all_list = find_apartment_urls()
    # url_all_list += find_urls()
    url_all_list = [

        'https://www.dabangapp.com/room/5e8c2e7efbefce1fe5167abd',
        'https://www.dabangapp.com/room/5e9e84a82813302220568899',
        'https://www.dabangapp.com/room/5ea1347909954739c5c9504f',
        'https://www.dabangapp.com/room/5e959ed59d092d2d947a6e82',
        'https://www.dabangapp.com/room/5e9577327452584ad2b23229',
        'https://www.dabangapp.com/room/5ea12f7eb5b0a50df78c80d4',
        'https://www.dabangapp.com/room/5ea12ff53604560df7209588',
        'https://www.dabangapp.com/room/5e9cf255b8b9d54ecb127b6d',
        'https://www.dabangapp.com/room/5ea12196911aae727274516c',
        'https://www.dabangapp.com/room/5e8293bb31c88476954f7213',
        'https://www.dabangapp.com/room/5ea13f89b9713b4014f00d09',
        'https://www.dabangapp.com/room/5e9830b9b663983579c58766',
        'https://www.dabangapp.com/room/5e7ad24a5809285b43dd6156',
        'https://www.dabangapp.com/room/5e9a6d46240f921ded23c612',
        'https://www.dabangapp.com/room/5e9a93546f87913df7e9a3c8',
        'https://www.dabangapp.com/room/5ea123f5b5044172720f27c4',
        'https://www.dabangapp.com/room/5e9e7a6676b64676929b5a19',
        'https://www.dabangapp.com/room/5e9d0e86d83b1c575d03a3a2',
        'https://www.dabangapp.com/room/5ea123dda257b9727276461b',
        'https://www.dabangapp.com/room/5e8eab2db72bfe784f349eb9',
        'https://www.dabangapp.com/room/5e93f2dcf452272015119987',
        'https://www.dabangapp.com/room/5e9d13593072960e0958b12e',
        'https://www.dabangapp.com/room/5ea14dea34c5c445b3e12a18',
        'https://www.dabangapp.com/room/5e982559ec85df024d33c6ff',
        'https://www.dabangapp.com/room/5e8c62242dca726fb8181a93',
        'https://www.dabangapp.com/room/5e81beab3da96b3251ddf7eb',
        'https://www.dabangapp.com/room/5ea13d20c487962cee5d8e1d',
        'https://www.dabangapp.com/room/5ea11e5b142e92049163a55e',
        'https://www.dabangapp.com/room/5e868a4369367f4ba04cbd9a',
        'https://www.dabangapp.com/room/5e993faad404b13eebefc07c',
        'https://www.dabangapp.com/room/5e9a801126b6362ef9643304',
        'https://www.dabangapp.com/room/5e919ebcf6898d237c673810',
        'https://www.dabangapp.com/room/5e9f966d5bff6f69c8e5269a',
        'https://www.dabangapp.com/room/5e7ac6c2cbf0df08eb1d61ff',
        'https://www.dabangapp.com/room/5e84665fdec4512c8b64192a',
        'https://www.dabangapp.com/room/5ea12af38c7c6101622b9739',
        'https://www.dabangapp.com/room/5ea12d58a0489228291ef92a',
        'https://www.dabangapp.com/room/5ea12cb938f5602829400125',
        'https://www.dabangapp.com/room/5e980174c176a611a8c08e2a',
        'https://www.dabangapp.com/room/5ea24657aaba051a6a2daad9',
        'https://www.dabangapp.com/room/5ea15bed9b68f41cd31be68f',
        'https://www.dabangapp.com/room/5e9d05fc0e86e0702e720c6e',
        'https://www.dabangapp.com/room/5e9e4be7a2089e2a1ea40848',
        'https://www.dabangapp.com/room/5e9a9586f8d6c15542e17680',
        'https://www.dabangapp.com/room/5e8ac6d37f0d924616315449',
        'https://www.dabangapp.com/room/5e9e67899c67b66a65db2727',
        'https://www.dabangapp.com/room/5e9d631a9ed0543d07893449',
        'https://www.dabangapp.com/room/5ea14be8a66c1345b3284e41',
        'https://www.dabangapp.com/room/5ea100f97e378c2fd6bcf605',
        'https://www.dabangapp.com/room/5e7afd8e99ef8a59f3a5afd9',
        'https://www.dabangapp.com/room/5e8aa4778e97eb10a32212da',
        'https://www.dabangapp.com/room/5ea14e14caceac45b3db6f09',
        'https://www.dabangapp.com/room/5ea13a4941df6448833e550f',
        'https://www.dabangapp.com/room/5e9001d9004a6b46f8e283bc',
        'https://www.dabangapp.com/room/5e950f7d8464a8139b87e2f9',
        'https://www.dabangapp.com/room/5e967dbc5448c97f566410e9',
        'https://www.dabangapp.com/room/5e8d636cdc19e6397ec46d1e',
        'https://www.dabangapp.com/room/5e9e4ec8ba19d04499b8d342',
        'https://www.dabangapp.com/room/5ea107a769d22940bb6dfb00',
        'https://www.dabangapp.com/room/5e991207f8626e52174025fa',
        'https://www.dabangapp.com/room/5e8be7742fa6cd03e13c708b',
        'https://www.dabangapp.com/room/5e8ab2d3e5b96224197411d8',
        'https://www.dabangapp.com/room/5e990448a2d17027c7d5a1be',
        'https://www.dabangapp.com/room/5ea14ef101a9a858d050e301',
        'https://www.dabangapp.com/room/5e9e7a1a3275bd3dedfbadbf',
        'https://www.dabangapp.com/room/5ea109a2bcb6b164ec1a2691',
        'https://www.dabangapp.com/room/5ea142cfb73840591f4f7a40',
        'https://www.dabangapp.com/room/5ea1314c4cf97210f91da51e',
        'https://www.dabangapp.com/room/5e7ad2422247205b43406c05',
        'https://www.dabangapp.com/room/5e8ec761980d512302d88076',
        'https://www.dabangapp.com/room/5e9a8085ec0d5e2ef92ba4b0',
        'https://www.dabangapp.com/room/5e8ac3f8d5f8af65d9d3516d',
        'https://www.dabangapp.com/room/5ea130087c10e30df70638d2',
        'https://www.dabangapp.com/room/5ea1316c60d6c010f91a2c93',
        'https://www.dabangapp.com/room/5e95402d89c3f624a200b096',
        'https://www.dabangapp.com/room/5e8fed22182fb750ac3ed90c',
        'https://www.dabangapp.com/room/5ea108010bc55f40bb3205d7',
        'https://www.dabangapp.com/room/5ea123c930ea92727225f95f',
        'https://www.dabangapp.com/room/5e82935402a1f77695464902',
        'https://www.dabangapp.com/room/5ea121ae1e015772727aca06',
        'https://www.dabangapp.com/room/5e991254697bff521708eeb6',
        'https://www.dabangapp.com/room/5e9a567d8d0d5c5d3e33e247',
        'https://www.dabangapp.com/room/5ea14e016addd145b3ec8dc3',
        'https://www.dabangapp.com/room/5e9d9148b9fe4f38991401fa',
        'https://www.dabangapp.com/room/5ea153fc23360a602a5b3dff',
        'https://www.dabangapp.com/room/5e941f861343d9304c095c33',
        'https://www.dabangapp.com/room/5ea136d2b79f505fbd1ac062',
        'https://www.dabangapp.com/room/5e8e87131a056b7de982d60c',
        'https://www.dabangapp.com/room/5ea0fb5d87659f3690c3010f',
        'https://www.dabangapp.com/room/5e7c13ee116bff1a5c1b0fe5',
        'https://www.dabangapp.com/room/5e9a9d28f3c5cc720adcf372',
        'https://www.dabangapp.com/room/5ea11d665478006b87d097a9',
        'https://www.dabangapp.com/room/5e81aed624e07a1c823c3867',
        'https://www.dabangapp.com/room/5e9818a86240cf50e9caced0',
        'https://www.dabangapp.com/room/5e9a6dbe897ecf1ff2965b20',
        'https://www.dabangapp.com/room/5ea1445d636ba07f16d4646c',
        'https://www.dabangapp.com/room/5e7c36033dc51b7e45ba7b1f',
        'https://www.dabangapp.com/room/5e819e0e2ce1b126d9c88027',
        'https://www.dabangapp.com/room/5ea13fa42061014014fac2a4',
        'https://www.dabangapp.com/room/5e9d5e4e42d946527da08d99',
        'https://www.dabangapp.com/room/5e9579612464e04ad27f0f71',
        'https://www.dabangapp.com/room/5e8ae5dd2a140b19ad1152a0',
        'https://www.dabangapp.com/room/5ea109f0d044dc64ec9e83c4',
        'https://www.dabangapp.com/room/5ea254ea23e2d246388705c9',
        'https://www.dabangapp.com/room/5ea11daa6ad99a6b87825030',
        'https://www.dabangapp.com/room/5e9e81dad2c65a036b6485a2',
        'https://www.dabangapp.com/room/5e7ae6cdfccb516fda9bd67a',
        'https://www.dabangapp.com/room/5e96749059ccda73850bed67',
        'https://www.dabangapp.com/room/5e98255d2d3292024de08380',
        'https://www.dabangapp.com/room/5e8ff5dc57abf65d42b86d86',
        'https://www.dabangapp.com/room/5ea2552c64929146382c4d05',
        'https://www.dabangapp.com/room/5e9d77fa86a7380414e4fe0f',
        'https://www.dabangapp.com/room/5e7c0280a77db85208d4fc64',
        'https://www.dabangapp.com/room/5e8e76abab03dd31e56dcb71',
        'https://www.dabangapp.com/room/5e814fd64039fb0ab049a6d8',
        'https://www.dabangapp.com/room/5e86f4b7e302b11c09fae313',
        'https://www.dabangapp.com/room/5e8a945fee38c71dd70b0cb0',
        'https://www.dabangapp.com/room/5e8aac2b54de271a14e4c32e',
        'https://www.dabangapp.com/room/5e85790803871a2aa7b0afdb',
        'https://www.dabangapp.com/room/5e8d6e4dd2170c747784db4e',
        'https://www.dabangapp.com/room/5e93d59f0d890e350fde4db7',
        'https://www.dabangapp.com/room/5e9d03625b11645964c6cba4',
        'https://www.dabangapp.com/room/5e9a828f0d68674507df2f6f',
        'https://www.dabangapp.com/room/5e8550aabea97b7a22578734',
        'https://www.dabangapp.com/room/5e8154e74cd9607c21f9d10c',
        'https://www.dabangapp.com/room/5e7c3a23c85f5376a60e8fc9',
        'https://www.dabangapp.com/room/5e7ac451a96dd2389c19493c',
        'https://www.dabangapp.com/room/5e9146a83fb2521b2c49ecee',
        'https://www.dabangapp.com/room/5e7d6469c88b2e4d3edf63ab',
        'https://www.dabangapp.com/room/5e8ae5ed851dda19ad8b717d',
        'https://www.dabangapp.com/room/5e9900c05b96152a30f1836c',
        'https://www.dabangapp.com/room/5e82b23608fecc73e61f4d63',
        'https://www.dabangapp.com/room/5e9d036138d59759645642c9',
        'https://www.dabangapp.com/room/5e856698c18a88387dfe7d10',
        'https://www.dabangapp.com/room/5e81610280554a6b432242ca',
        'https://www.dabangapp.com/room/5e81884c1e326a0478fe722b',
        'https://www.dabangapp.com/room/5e86a3c6c3bafd57a1dd6a77',
        'https://www.dabangapp.com/room/5e9d0a5700d23858ea339d3a',
        'https://www.dabangapp.com/room/5e97d58eaef5dd36e7d0546c',
        'https://www.dabangapp.com/room/5e95779ac7ba0c4ad2ccf748',
        'https://www.dabangapp.com/room/5e8edff144048f63141f001c',
        'https://www.dabangapp.com/room/5e940cdd1ce2ec3178760a38',
        'https://www.dabangapp.com/room/5e82d5bb15e93834534e5f52',
        'https://www.dabangapp.com/room/5e82b22081a85e73e67a5dda',
        'https://www.dabangapp.com/room/5e942123724aac304cd16dc8',
        'https://www.dabangapp.com/room/5e7ed445b9ca165a0abe5c37',
        'https://www.dabangapp.com/room/5e8830b78321b32902cade76',
        'https://www.dabangapp.com/room/5ea126699cd5531b825459c0',
        'https://www.dabangapp.com/room/5e61eb268c45fb4368c1a174',
        'https://www.dabangapp.com/room/5ea0f65f7fe6d517660c6615',
        'https://www.dabangapp.com/room/5ea0f659ff0f5117661c8408',
        'https://www.dabangapp.com/room/5e9435995c3ac1609a8fd908',
        'https://www.dabangapp.com/room/5e82ffe2f112a16b1126ca5e',
        'https://www.dabangapp.com/room/5e93ec571087be6c9d348d9c',
        'https://www.dabangapp.com/room/5e82f884d770ee57c7f381cf',
        'https://www.dabangapp.com/room/5e9fbc3505ff823c392d4d3a',
        'https://www.dabangapp.com/room/5ea0f65d8682c517622cd49d',
        'https://www.dabangapp.com/room/5e6759cdb979bc71e9afeab2',
        'https://www.dabangapp.com/room/5e4b99581a00fb457ff0ef63',
        'https://www.dabangapp.com/room/5e86edc1914a1d1d7ef51ac2',
        'https://www.dabangapp.com/room/5e9034ed4ef6ae3420ccbfb7',
        'https://www.dabangapp.com/room/5e8f01b3cec5d415e90d4cf6',
        'https://www.dabangapp.com/room/5ea0fcfd27599121780b30b1',
        'https://www.dabangapp.com/room/5ea0f5770eea072ac547b418',
        'https://www.dabangapp.com/room/5d64b386c2523c16a42f3d07',
        'https://www.dabangapp.com/room/5e97be37ebb9bb57a7d35d5f',
        'https://www.dabangapp.com/room/5e9fd19bdea9fc5a7d8f5173',
        'https://www.dabangapp.com/room/5e9a9a61cd736f6ba9c09bfd',
        'https://www.dabangapp.com/room/5e994fc856dddc1856281d59',
        'https://www.dabangapp.com/room/5e6f0321aeeb591276221de3',
        'https://www.dabangapp.com/room/5d8ee7ac7fa17e2f2267239a',
        'https://www.dabangapp.com/room/5e9a7799f2ccbd48e3c5b08f',
        'https://www.dabangapp.com/room/5e967aa03b72e37c4b8e19f4',
        'https://www.dabangapp.com/room/5e9febd7bf530716fcbf51c5',
        'https://www.dabangapp.com/room/5e3845a2d7447c3fabc904e3',
        'https://www.dabangapp.com/room/5e843dc1031dc142631601df',
        'https://www.dabangapp.com/room/5e996a9b7accce730023773e',
        'https://www.dabangapp.com/room/5e9efb294b187c5a8beb346f',
        'https://www.dabangapp.com/room/5e843a4d99a00c17e3bc85c4',
        'https://www.dabangapp.com/room/5e0f3718d96bea310291e09a',
        'https://www.dabangapp.com/room/5e9eb0fc7145c11ebb232db9',
        'https://www.dabangapp.com/room/5e992d3359f24d63d2c5afc2',
        'https://www.dabangapp.com/room/5e9d038f618ea701e1304f33',
        'https://www.dabangapp.com/room/5ea0e60d5602871b03ab5838',
        'https://www.dabangapp.com/room/5e9eb9a7db13d21edb07f96e',
        'https://www.dabangapp.com/room/5ea0f58193c1372ac2df539f',
        'https://www.dabangapp.com/room/5e9d03b0eb4f8f27a0b1c0a2',
        'https://www.dabangapp.com/room/5e816497deec6b3194f63705',
        'https://www.dabangapp.com/room/5e71af111d650303159f0348',
        'https://www.dabangapp.com/room/5e9a82fd7329a5563a77274e',
        'https://www.dabangapp.com/room/5df1ea294eac3d7bfabcba03',
        'https://www.dabangapp.com/room/5e870376f429084ca09bcea6',
        'https://www.dabangapp.com/room/5e84034e55c6882f23bd690e',
        'https://www.dabangapp.com/room/5e58feb4bab02104722d161f',
        'https://www.dabangapp.com/room/5e8ace5e7702c43897f858ac',
        'https://www.dabangapp.com/room/5e99104de7921f1d798272a3',
        'https://www.dabangapp.com/room/579704dc6f1b3a094aec5f57',
        'https://www.dabangapp.com/room/5d9c54de54340c1c977f92d8',
        'https://www.dabangapp.com/room/5e33bb027bfab713de85a774',
        'https://www.dabangapp.com/room/5df1eb02d5887d7930797275',
        'https://www.dabangapp.com/room/5e9192b1afa34c2320474d61',
        'https://www.dabangapp.com/room/5e99601abc1a2e63758d1968',
        'https://www.dabangapp.com/room/5e91566b0f96861e75b1b60f',
        'https://www.dabangapp.com/room/5e94139c0eb4bb3b5f8d29c4',
        'https://www.dabangapp.com/room/5ea2407f78300f59a0c339b5',
        'https://www.dabangapp.com/room/5e3bd8f8a44600193619046c',
        'https://www.dabangapp.com/room/5e9c6094fbacbb09194f76ba',
        'https://www.dabangapp.com/room/59f3e67dc6cda31e4c4f8b33',
        'https://www.dabangapp.com/room/5dc282ff3c2c224b0a79097c',
        'https://www.dabangapp.com/room/5e659c74f2a3ac415c367599',
        'https://www.dabangapp.com/room/5de1e3dcbff13320f9e8c246',
        'https://www.dabangapp.com/room/5e24669efd66bf3f32346a69',
        'https://www.dabangapp.com/room/5e84996da1218276a29e79cc',
        'https://www.dabangapp.com/room/5e9a9ccf17b6ea61206f3133',
        'https://www.dabangapp.com/room/5d89b7deb3be6628c11e79d4',
        'https://www.dabangapp.com/room/5e9d039eedc091134efbe315',
        'https://www.dabangapp.com/room/582fb3c519e7cb55ecce2534',
        'https://www.dabangapp.com/room/5e268a6db427ae304ec68e3f',
        'https://www.dabangapp.com/room/5e9d0381baaea321eaa3e34f',
        'https://www.dabangapp.com/room/5c5d8557e98ed333425a3cb4',
        'https://www.dabangapp.com/room/5e7c52a336e37e1fa669f93e',
        'https://www.dabangapp.com/room/5e9d2721b233a17b687cb304',
        'https://www.dabangapp.com/room/5e8d36c5643ef26fe5d7a23a',
        'https://www.dabangapp.com/room/5e7866f0485b277642a0bea0',
        'https://www.dabangapp.com/room/5e3cfc049d81167ed198e975',
        'https://www.dabangapp.com/room/5e996005faf976637565726a',
        'https://www.dabangapp.com/room/5e99621f39378058bf1c015e',
        'https://www.dabangapp.com/room/5e7997c5619be26de13760d1',
        'https://www.dabangapp.com/room/5ea11deceb27865ced4c9866',
        'https://www.dabangapp.com/room/5d1aaaf7f8675e2ee22fd097',
        'https://www.dabangapp.com/room/5e61de5954444f17b12b891d',
        'https://www.dabangapp.com/room/5db78bcdeaa0e9359de71c0f',
        'https://www.dabangapp.com/room/5e6132798c88164b71a43b63',
        'https://www.dabangapp.com/room/5e9d038861e7bf04feff40cc',
        'https://www.dabangapp.com/room/5da4831a99f821789dd5a462',
        'https://www.dabangapp.com/room/5e8440d00fdecc72da927bf7',
        'https://www.dabangapp.com/room/5e9d0377c07c9e12a226f2bb',
        'https://www.dabangapp.com/room/581ae8a8f7f1fe26fd7d65f0',
        'https://www.dabangapp.com/room/5e843414848c0b61944e50c5',
        'https://www.dabangapp.com/room/5c8319179435f455bfadb906',
        'https://www.dabangapp.com/room/5ddd53a496557639e70c825e',
        'https://www.dabangapp.com/room/5e577c56e868473adfb353ff',
        'https://www.dabangapp.com/room/5e8e89360988e55bd5c27df0',
        'https://www.dabangapp.com/room/5d07c75b3742fe7603630b43',
        'https://www.dabangapp.com/room/5e958f3d320e1034a235c14c',
        'https://www.dabangapp.com/room/5e8c077fc6addb21400412cb'
        'https://www.dabangapp.com/room/5e992d31d9d3a15c88491696',
        'https://www.dabangapp.com/room/5e9efb20350ca26a1cb134db',
        'https://www.dabangapp.com/room/5e9efb251e60da5787550276',
        'https://www.dabangapp.com/room/5e9fd1f1a639766eb587c9fc',
        'https://www.dabangapp.com/room/5e992d30f30bdb6390449f94',
        'https://www.dabangapp.com/room/5e9e60010f85d2751c0ff977',
        'https://www.dabangapp.com/room/5ea1349d913a6639c5e54238',
        'https://www.dabangapp.com/room/5ea13ff0aad7c6401418b249',
        'https://www.dabangapp.com/room/5e901025f3ff9d77d2ee73f7',
        'https://www.dabangapp.com/room/5e8ab2a116fdf52419a4663e',
        'https://www.dabangapp.com/room/5ea12ae6553a4d016280bbb2',
        'https://www.dabangapp.com/room/5e857bc1b4e0795b8a572512',
        'https://www.dabangapp.com/room/5e8d77eec22836604787ccb7',
        'https://www.dabangapp.com/room/5ea15bec9e83bd1cd30c0dd7',
        'https://www.dabangapp.com/room/5e8ae5d9ff822c19ad4d0911',
        'https://www.dabangapp.com/room/5ea142c0b2c041591f081e8a',
        'https://www.dabangapp.com/room/5e990650191cf83bfeb9b2ff',
    ]
    #
    # url_all_list = ['https://www.dabangapp.com/room/5e857bc1b4e0795b8a572512']
    # 각 게시글 조회 시작
    for post_index, url in enumerate(url_all_list):
        print('############################################# 다음 url \n')
        print('url 입니다.', url, '\n')
        driver.get(url)

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
        # button = driver.find_element_by_xpath("/html/body/div[4]/div/div/header/button")
        # driver.execute_script("arguments[0].click();", button)

        broker_ins = Broker.objects.get_or_create(
            companyName=companyName,
            address=address,
            managerName=managerName,
            tel=tel,
            image=test_url[0],
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
                    unrefined_parking = driver.find_elements_by_xpath(
                        '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[4]/p')
            else:
                if salesType == "매매":
                    try:
                        unrefined_parking = driver.find_elements_by_xpath(
                            "/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[3]")
                    except IndexError:
                        unrefined_parking = driver.find_elements_by_xpath(
                            '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[3]/p')
                else:
                    unrefined_parking = driver.find_elements_by_xpath(
                        "/html/body/div[1]/div/div[5]/div[2]/div/table/tbody/tr/td[4]/p")

            if 'unrefined_parking' in locals():
                print('없')
                try:
                    parkingDetail = driver.find_element_by_xpath(
                        '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[4]/p')
                    parkingDetail = parkingDetail.get_attribute('innerText')
                except NoSuchElementException:
                    unrefined_parking = driver.find_elements_by_xpath(
                        '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[3]/p')
            print('parkingDetail>>', parkingDetail)
            print('parkingTF >>', parkingTF)
            if 'unrefined_parking' in locals():
                parkingDetail = unrefined_parking[0].get_attribute('innerText')
            if 'parkingDetail' in locals():
                if '만' in parkingDetail:
                    parkingPay = parkingDetail
                    parkingPay = parkingPay.split('만')
                    parkingPay = parkingPay[0]
                    print('parkingPay >> ', parkingPay)
                    parkingPay = float(parkingPay)
                    print(type(parkingPay))

                    parkingDetail = '문의'
        except IndexError:
            unrefined_parking = driver.find_elements_by_xpath(
                '/html/body/div[1]/div/div[5]/div[3]/div/table/tbody/tr/td[4]/p'
            )
            if type(parkingDetail) == str:
                pass
            else:
                parkingDetail = unrefined_parking[0].get_attribute('innerText')

                if '만' in parkingDetail:
                    parkingPay = parkingDetail
                    parkingDetail = '문의'

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
            # broker=broker_ins[0],
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
