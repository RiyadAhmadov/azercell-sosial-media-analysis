from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service

with open("account_info.txt", "r", encoding="utf-8") as file:
    lines = file.read().strip().split("\n")

USERNAME = lines[0].strip()
PASSWORD = lines[1].strip()

chrome_driver_path = "chromedriver.exe"
service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service)
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(5)

username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")
username_input.send_keys(USERNAME)
time.sleep(2)
password_input.send_keys(PASSWORD)
time.sleep(2)
password_input.send_keys(Keys.RETURN)
time.sleep(5)

page_url = "https://www.instagram.com/azercell/"
driver.get(page_url)
time.sleep(5)

post_links = set() 
scroll_count = 0
max_scrolls = 100 
target_posts = 500
no_new_posts_threshold = 5

while len(post_links) < target_posts and scroll_count < max_scrolls:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  

    posts = driver.find_elements(By.XPATH, '//a[contains(@href, "/p/")]')
    new_posts = 0
    for post in posts:
        link = post.get_attribute("href")
        if link and link not in post_links:
            post_links.add(link)
            new_posts += 1
            if len(post_links) >= target_posts:
                break

    scroll_count += 1

    if new_posts == 0:
        no_new_posts_threshold -= 1
        if no_new_posts_threshold == 0:
            break
    else:
        no_new_posts_threshold = 5  

df = pd.DataFrame(list(post_links)[:target_posts], columns=["Post Links"])
df.to_excel('post_links_500.xlsx', index=False)

driver.quit()