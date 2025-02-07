from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("account_info.txt", "r", encoding="utf-8") as file:
    lines = file.read().strip().split("\n")

USERNAME = lines[2].strip()
PASSWORD = lines[3].strip()

chrome_driver_path = "chromedriver.exe"
service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service)
driver.get("https://www.instagram.com/accounts/login/")
driver.maximize_window()
time.sleep(5) 

links = pd.read_excel("instagram_posts.xlsx")

username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")
username_input.send_keys(USERNAME)
time.sleep(2)
password_input.send_keys(PASSWORD)
time.sleep(2)
password_input.send_keys(Keys.RETURN)
time.sleep(10)

def scrape_comments(post_url):
    driver.get(post_url)
    time.sleep(5) 

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    post_content = soup.find_all('div', class_="xt0psk2")
    post_title = post_content[0].text.strip() if post_content else "Unknown"

    comments = soup.find_all('span', class_="_ap3a _aaco _aacu _aacx _aad7 _aade")

    usernames = soup.find_all('a', class_="x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp xqnirrm xj34u2y x568u83")
    username_texts = [username.text.strip() for username in usernames]

    time_tag = soup.find('time', class_="x1p4m5qa")
    date_part, time_part = (time_tag['datetime'].split('T') if time_tag else ("Unknown", "Unknown"))

    post_comments, comment_dates, post_contents, user_names, like_counts, post_images = [], [], [], [], [], []

    for i, comment in enumerate(comments):
        comment_text = comment.text.strip()
        post_comments.append(comment_text)
        username = username_texts[i+1] if i < len(username_texts) else "Unknown"
        user_names.append(username)
        
        comment_time_tag = comment.find_parent('li').find('time')
        comment_date = comment_time_tag['datetime'].split('T')[0] if comment_time_tag else "Unknown"
        comment_dates.append(comment_date)

        post_contents.append(post_title)
        
        likes_span = comment.find_parent('li').find('span', class_='x193iq5w')
        if likes_span:
            likes_match = [text.strip() for text in likes_span.stripped_strings if "like" in text]
            likes_text = likes_match[0] if likes_match else "0 like"
        else:
            likes_text = "0 like"
        like_counts.append(likes_text)

    image_elements = driver.find_elements(By.CLASS_NAME, 'x5yr21d.xu96u03.x10l6tqk.x13vifvy.x87ps6o.xh8yej3')
    image_urls = [img.get_attribute('src') for img in image_elements]
    
    post_images = [", ".join(image_urls)] * len(post_comments)  
    
    post_like_span = soup.find('span', class_="x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj")
    if post_like_span:
        post_like_count = post_like_span.find_next('span', class_="html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs")
        post_like_count = post_like_count.text.strip() if post_like_count else "0"
    else:
        post_like_count = "0"


    post_comments_df = pd.DataFrame({
        'Username': user_names,
        'Comments': post_comments,
        'Date': date_part,
        'Time': time_part,
        'Comment Date': comment_dates,
        'Post Content': post_contents,
        'Likes': like_counts,
        'Post Likes': post_like_count,
        'Images': post_images
    })

    return post_comments_df

all_comments_df = pd.DataFrame()

for post_url in links['Post Links'].to_list():
    df = scrape_comments(post_url)
    all_comments_df = pd.concat([all_comments_df, df], ignore_index=True)

all_comments_df.to_excel(r'C:\Users\HP\OneDrive\İş masası\azercell_instagram_comments2.xlsx', index=False)

driver.quit()