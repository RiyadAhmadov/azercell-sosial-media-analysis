import pickle
import time
import sys
import io
import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

chrome_driver_path = "chromedriver.exe"
service = Service(chrome_driver_path)

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled") 
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.facebook.com/")

try:
    cookies = pickle.load(open("facebook_cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
except Exception as e:
    driver.quit()
    sys.exit()

video_posts_file = 'facebook_posts.xlsx'
df_links = pd.read_excel(video_posts_file)
video_links = df_links['Post Links'].tolist()  

comments_data = []

def load_all_comments(max_attempts=10):
    previous_count = 0 
    attempts = 0 

    while attempts < max_attempts:
        more_comments_buttons = driver.find_elements(By.XPATH, "//div[contains(@class, 'x1i10hfl xjbqb8w xjqpnuy') and not(contains(@aria-label, 'Like'))]")
        current_count = len(more_comments_buttons)

        if current_count == previous_count:
            break

        for button in more_comments_buttons:
            try:
                driver.execute_script("arguments[0].click();", button)
                time.sleep(random.uniform(2, 4)) 
            except Exception as e:
                continue

        previous_count = current_count
        attempts += 1  


def scroll_down():
    for _ in range(10):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(random.uniform(2, 4))

comments_data = []

def extract_comments():
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='x1lliihq xjkvuk6 x1iorvi4']"))
        )

        comment_elements = driver.find_elements(By.XPATH, "//div[@class='x1lliihq xjkvuk6 x1iorvi4']")

        username_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'xwib8y2 xn6708d x1ye3gou x1y1aw1k')]//span[contains(@class, 'xt0psk2')]//span[contains(@class, 'xjp7ctv')]//a[contains(@class, 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1s688f')]//span[contains(@class, 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa x1s688f xzsf02u')]")

        time_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'x6s0dn4 x3nfvp2')]//ul[contains(@class, 'html-ul xe8uvvx xdj266r x4uap5 x18d9i69 xkhd6sd x1n0m28w x78zum5 x1wfe3co xat24cr xsgj6o6 x1o1nzlu xyqdw3p')]//li[contains(@class, 'html-li xdj266r xat24cr xexx8yu x4uap5 x18d9i69 xkhd6sd x1rg5ohu x1emribx x1i64zmx')]//span[contains(@class, 'x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j')]//div[contains(@class, 'html-div xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd')]//a[contains(@class, 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1sur9pj xkrqix3 xi81zsa x1s688f')]")

        image_element = driver.find_element(By.XPATH, "//div[contains(@class, 'x6s0dn4 x78zum5 xdt5ytf xl56j7k x1n2onr6')]//img")
        image_src = image_element.get_attribute("src") if image_element else None

        for username_elem, comment_elem, time_elem in zip(username_elements, comment_elements, time_elements):
            username = username_elem.text.strip() if username_elem else "Unknown"
            comment = comment_elem.text.strip() if comment_elem else None
            comment_time = time_elem.text.strip() if time_elem else None

            if comment and comment_time:
                comments_data.append({
                    "Username": username,
                    "Comment": comment,
                    "Comment Time": comment_time,
                    "Image": image_src
                })

    except Exception as e:
        print(f"Error {e}")

for idx, link in enumerate(video_links):
    driver.get(link)
    time.sleep(random.uniform(5, 8))
    scroll_down()
    load_all_comments()
    extract_comments()

df_comments = pd.DataFrame(comments_data)

output_comments_path = 'facebook_video_comments.xlsx'
df_comments.to_excel(output_comments_path, index=False)

driver.quit()
