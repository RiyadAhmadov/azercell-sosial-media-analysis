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

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

chrome_driver_path = "chromedriver.exe"
service = Service(chrome_driver_path)

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled") 
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

page_url = "https://www.facebook.com/azercell/photos"
driver.get(page_url)
time.sleep(10)  

post_links = set()
target_posts = 500
scroll_attempts = 0
max_scrolls = 200  

while len(post_links) < target_posts and scroll_attempts < max_scrolls:
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(random.uniform(3, 6))  

    elements = driver.find_elements(By.XPATH, '//a[contains(@href, "photo.php?fbid=")]')

    for element in elements:
        href = element.get_attribute("href")
        if href and "photo.php?fbid=" in href:
            post_links.add(href.split("&")[0])

    scroll_attempts += 1

    if len(post_links) >= target_posts:
        break

df = pd.DataFrame({'Post Links': list(post_links)})

output_path = 'facebook_posts.xlsx'
df.to_excel(output_path, index=False)

driver.quit()
