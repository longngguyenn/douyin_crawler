from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.service import Service
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

def convert_to_decimal(str):
    if str.endswith('万'):
        decimal_number = float(str.replace('万', ''))*10000
    else:
        decimal_number = float(str)
    return decimal_number

def get_link(file, x=0.8): #execute dom_tree to links with x% top video
    with open(file, 'r', encoding='utf-8') as file_dom_tree:
        dom_tree = file_dom_tree.read()
    pattern = r'(/video/\d{19}).*?>([\d.]+万?)</span>'
    matches = re.findall(pattern, dom_tree)
    # print(f'matches={matches}')
    videos_dict = {}
    for i, match in enumerate(matches):
        view = convert_to_decimal(match[1])
        
        link = match[0]
        
        videos_dict[i] = {'view': view, 'link': link}
        # print("video views = ",videos[i]['view'])
    n = len(matches)
    k = int(x*n)+3
    #Take out top k videos with highest view
    top_view_videos = sorted(videos_dict.items(), key=lambda x:x[1]['view'], reverse=True)[:k]
    video_links = []
    for video in top_view_videos:
        video_links.append('https://www.douyin.com'+str(video[1]['link']))
    return video_links

# INPUT: nothing | OUTPUT: driver
def launch_chrome_profile(download_path=r"C:\Users\khanh\Downloads\Xiaohongshu\music", profile_path = r'C:\\Users\\khanh\\AppData\\Local\\Google\\Chrome\\User Data', profile = 'Profile 2'):
    
    global driver
    if driver is None:
    
            # Set Chrome options
            chrome_options = Options()
            chrome_options.add_argument(f"user-data-dir={profile_path}")  # Path to your chrome profile
            chrome_options.add_argument(f"--profile-directory={profile}")
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            # chrome_options.add_argument('--ignore-certificate-errors')
            # chrome_options.add_argument('--ignore-ssl-errors')
            chrome_options.add_argument('--disk-cache-size=0')
            # Set Chrome preferences
            prefs = {"profile.default_content_settings.popups": 0,
                    "download.default_directory": download_path,
                    "download.directory_upgrade": True,}

            chrome_options.add_experimental_option("prefs", prefs)

            # Set up Chrome service
            service = Service(ChromeDriverManager().install())

            # Launch Chrome
            driver = webdriver.Chrome(service=service, options=chrome_options)
            return driver
    else:
        return driver

def crawl_domtree(douyin_user_link): #=> return the domtree.txt file
    driver = launch_chrome_profile()
    driver.get(douyin_user_link)
    sleep(random.uniform(10,20))

    print('\nScrolling windows to the end\n')
    for _ in range(3):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        sleep(3)
    sleep(random.uniform(10,20))
    dom_tree = 'douyin_dom_tree.txt' 
    with open(dom_tree, 'w', encoding='utf-8') as f:
        f.write(driver.execute_script('return document.documentElement.outerHTML'))
    return dom_tree

def download_links_TRASH(video_links):
    chrome_options = webdriver.ChromeOptions()
    service = Service(executable_path=r"C:\Users\khanh\OneDrive - UMP\LFCde\chromedriver.exe")

    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--disk-cache-size=0')
    base_download_dir = r"C:\Users\khanh\Downloads\Girl_douyin"
    download_dir = os.path.join(base_download_dir,'Girl_1')
    chrome_options.add_experimental_option('prefs', {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    driver = webdriver.Chrome(options = chrome_options, service=service)
    driver.delete_all_cookies()

    undownload = []
    for i in range(0,len(video_links),1):
        link = video_links[i]
        try:
            driver.get('https://snaptik.app/en/douyin-downloader')
            sleep(random.uniform(2,4))
            driver.find_element(By.CSS_SELECTOR,"[placeholder='Paste TikTok link here']").send_keys(link)
            sleep(2)
            driver.find_element(By.CSS_SELECTOR,"[placeholder='Paste TikTok link here']").submit()
            sleep(random.uniform(2,4))
            tempt_file = 'tempt_file.txt' 
            with open(tempt_file, 'w', encoding='utf-8') as f:
                f.write(driver.execute_script('return document.documentElement.outerHTML'))
            sleep(3)
            with open('tempt_file.txt', 'r', encoding='utf-8') as f:
                tempt_file = f.read()
            pattern = r'class="video-links"><a\shref="(.*?)"\sclass="button\sdownload-file\smt-3'
            match = "https://snaptik.app"+re.search(pattern, tempt_file).group(1).replace('amp','').replace(';','')
            # print(match)
            driver.get(match)
            sleep(random.uniform(3,8))
        except:
            undownload.append(link)
    return undownload

# INPUT: list links, driver, downloadpage, CSS_selector | OUTPUT: download video to download folder
def download_link(link, download_page ='https://snaptik.app/en/douyin-downloader'):
    driver = launch_chrome_profile()
    
    def down():
        driver.get(download_page)
        driver.find_element(By.CSS_SELECTOR,"[placeholder='Paste TikTok link here']").send_keys(link)
        driver.find_element(By.CSS_SELECTOR,"[placeholder='Paste TikTok link here']").submit()

        sleep(5)
        driver.find_element(By.CSS_SELECTOR,"[class='button download-file']").click() 
    attempts = 0
    max_attempts = 2
    while attempts < max_attempts:
        try:
            down()
            break  # If down() is successful, break the loop
        except NoSuchElementException:
            attempts += 1
            print(f"Attempt {attempts} failed with error: {NoSuchElementException}")
            if attempts == max_attempts:
                print(f"\nGiving up after 2 failed attempts.\n{link}\n")
                # with open('tempt_2.txt','a',encoding='utf-8') as f:
                    
                #     f.write('\n'+link)
                pass       

string = """
https://www.douyin.com/user/MS4wLjABAAAAuwV3CZZJPU5nBKBc9gPzouVO2tsfHNuaaWh9PqeqPqK9oiWf0dJrQCK26MJr4DOd
https://www.douyin.com/user/MS4wLjABAAAAjkxEqv9RZpMM0xjx47czGeyZUJiVlWlCCL2kXSUptaNSs4e8fjbL7jW1vnigGeC-?relation=0&vid=7292589455599242515
https://v.douyin.com/iYFuoWLY
https://v.douyin.com/iYFH2yuB
https://v.douyin.com/iYFHkLey
https://v.douyin.com/iYFHQgme
https://v.douyin.com/iYFHq61W
https://v.douyin.com/iYFHQgET
https://v.douyin.com/iYFHkusH
https://v.douyin.com/iYFHBsvf
https://v.douyin.com/iYFHhJk5
https://v.douyin.com/iYFH5UPh
https://v.douyin.com/iYFHHgMG
https://v.douyin.com/iYFKMXwp
https://v.douyin.com/iYFEVV6P
https://v.douyin.com/iYYdHoJ2
"""

douyin_user_links = [link for link in string.split('\n') if link.strip() != '']

""" Dong link nay chua cao luon ne

https://www.douyin.com/user/MS4wLjABAAAAfxl9DXFi2cgcTgZzsnBgnu8Kdv9oW7QkrM4s1MF3XdOqvNY6XfRNkPs4vY35cQns

https://www.douyin.com/user/MS4wLjABAAAA7tO1rWAStkFVbxytZhGvQOjSMSwRSCg5cbebSK9Cddw?vid=7261799444201491746

https://www.douyin.com/user/MS4wLjABAAAAhEmek_LQx2LZ0uWp4-WTObWDFo5hoX86_KEU9o9yr9u0dJZGcwM88nSqhskKWwpb?vid=7269757855878614311
0.8

https://www.douyin.com/user/MS4wLjABAAAADsd4u9PA-SPBHtQmymDatQsv3h8LG7gHJFEnAT2BHuI?vid=7259613131956063545
0.8https://www.xiaohongshu.com/explore/6426871a0000000013031768


https://www.douyin.com/user/MS4wLjABAAAArQGaYHuKpPPc0jkz7N9l7IMH6xcOiWCFDIlRjzqQ6UA
0.9

https://www.douyin.com/user/MS4wLjABAAAA7zPLDz1CBMR3tX_6qWDpt9me1lCjYtl2PLd2rLR9vBOKCZtEQKbnJ_GZqQxECD2i?vid=7269412701128936765

"""

""" List douyin le https://v.douyin.com/iJGfFnpL/
0.07 mDh:/ 数学老师是体育老师教的，跳舞老师是数学老师来的。# 每日一舞心情愉悦  https://v.douyin.com/iJGf1vWS/ 复制此链接，打开Dou音搜索，直接观看视频！
4.17 lca:/ 世界上最稳定噶关系，系我同你关系，不像恋人又不是结婚对象，不清楚到底为什么。@爱情短片  https://v.douyin.com/iJGfdH4J/ 复制此链接，打开Dou音搜索，直接观看视频！
9.76 reO:/ 19分钟60多万赞我


塞的女孩 # 这样的身材打几分 # 在

1.51 OKw:/ 我也有小🐶# vlog # vlog日常  https://v.douyin.com/iJGf5DWv/ 复制此链接，打开Dou音搜索，直接观看视频！

6.41 rrr:/ 今日是瑜伽女孩# 瑜伽 # 健身 # 瑜伽裤 # 运动女孩 # 美女瑜伽  https://v.douyin.com/iJGfxtH9/ 复制此链接，打开Dou音搜索，直接观看视频！

3.30 EHV:/ 周一早上，上班# 这样的身材有人喜欢吗 # 美女 # 是你的理想女朋友吗 # 穿搭 # 很哇塞的小姐姐 # 520约会穿搭可以安排啦  https://v.douyin.com/iJGfmw2d/ 复制此链接，打开Dou音搜索，直接观看视频！

3.30 BTY:/ 七夕文案 一人一句# ootd穿搭 # 开箱视频 # 今天穿什么 # 七夕  https://v.douyin.com/iJGf9NaT/ 复制此链接，打开Dou音搜索，直接观看视频！

9.94 aaN:/ 期待不期而遇# 穿搭 # 反差 # 纯欲天花板  https://v.douyin.com/iJGfKHk5/ 复制此链接，打开Dou音搜索，直接观看视频！

0.07 KWm:/ 请和我交往吧# 不愧是jk # 07@抖音小助手  https://v.douyin.com/iJGfGo3s/ 复制此链接，打开Dou音搜索，直接观看视频！

1.58 pDH:/ hi# 纯御  https://v.douyin.com/iJGfcGAH/ 复制此链接，打开Dou音搜索，直接观看视频！

5.66 ban:/ ^_^# jk妹是无敌的  https://v.douyin.com/iJGPYy9Q/ 复制此链接，打开Dou音搜索，直接观看视频！

9.97 ULJ:/ 选择题：法拉利和我，你选哪个# 性感丰满 # 黑丝搭配 # 反差 # 极品身材 # 性感可爱  索，直接观看视频！
5.30 Jip:/ 你那没品味的兄弟肯定刷不到# 浅跳一下  链接，打开Dou音搜索，直接观看视频！

3.84 lcn:/ # 吃鸡舞 # 微胖  https://v.douyin.com/iJGPH84b/ 复制此链接，打开Dou音搜索，直接观看视频！

7.61 kPx:/ 耶耶耶# 耶耶耶 # 微胖女生 # 浅跳一下  https://v.douyin.com/iJGP5YxC/ 复制此链接，打开Dou音搜索，直接观看视频！

2.56 kcN:/ 一天三更 还有谁# 浅跳一下  https://v.douyin.com/iJGPk2Qp/ 复制此链接，打开Dou音搜索，直接观看视频！

"""
if __name__=='__mains__':
    douyin_user_link = "https://www.douyin.com/user/MS4wLjABAAAAfxl9DXFi2cgcTgZzsnBgnu8Kdv9oW7QkrM4s1MF3XdOqvNY6XfRNkPs4vY35cQns"
    dom_tree = crawl_domtree(douyin_user_link=douyin_user_link)
    video_links = get_link(dom_tree, x = 0.3)
    print(f'\nThere are {len(video_links)} videos awaits')
    print(f'video_links={video_links}')
    
    
    tempt_list = download_links(video_links=video_links)
    while tempt_list !=[]:
        tempt_list = download_links(video_links=tempt_list)
        print(f"Remaining {len(tempt_list)}...")
    print('\nDONE ALL')

driver = None

for douyin_user_link in douyin_user_links:
    dom_tree = crawl_domtree(douyin_user_link)
    list_links = get_link(dom_tree,x=0.1)
    for link in list_links:
        download_link(link)
        


