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

def get_link(file, x=0.1): #execute dom_tree to links with x% top video
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
def launch_chrome_profile(profile_path = path_to_profile_chrome, profile = 'Profile_Name'):
    
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
    dom_tree = = driver.execute_script('return document.documentElement.outerHTML')

    return dom_tree
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

if "__name__"=="__main__":
    douyin_user_link = "https://www.douyin.com/user/MS4wLjABAAAAuwV3CZZJPU5nBKBc9gPzouVO2tsfHNuaaWh9PqeqPqK9oiWf0dJrQCK26MJr4DOd?relation=0&vid=7311331250793467187"
    driver = None
    for douyin_user_link in douyin_user_links:
    dom_tree = crawl_domtree(douyin_user_link)
    list_links = get_link(dom_tree,x=0.1)
    for link in list_links:
        download_link(link)
            


