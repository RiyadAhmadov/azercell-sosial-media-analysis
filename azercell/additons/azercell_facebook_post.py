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

# Set UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Paths
chrome_driver_path = r"C:\Users\HP\OneDrive\İş masası\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path)

# Start WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")  # Reduce bot detection
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.facebook.com/")

# Load saved cookies
try:
    cookies = pickle.load(open("facebook_cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    print("Logged in using cookies!")
except Exception as e:
    print("Error loading cookies:", e)
    driver.quit()
    sys.exit()

# Navigate to Facebook page
page_url = "https://www.facebook.com/azercell/photos"
driver.get(page_url)
time.sleep(10)  # Wait for page to load

# Scroll until we get at least 500 unique post links
post_links = set()
target_posts = 500
scroll_attempts = 0
max_scrolls = 200  # Safety limit to prevent infinite scrolling

while len(post_links) < target_posts and scroll_attempts < max_scrolls:
    # Scroll down
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(random.uniform(3, 6))  # Random sleep to mimic human behavior
    
    # Extract post links dynamically
    elements = driver.find_elements(By.XPATH, '//a[contains(@href, "photo.php?fbid=")]')

    for element in elements:
        href = element.get_attribute("href")
        if href and "photo.php?fbid=" in href:
            post_links.add(href.split("&")[0])  # Remove tracking params

    scroll_attempts += 1
    print(f"Scroll {scroll_attempts}: Collected {len(post_links)} post links...")

    # Stop if we reach 500+ posts
    if len(post_links) >= target_posts:
        break

# Save to DataFrame
df = pd.DataFrame({'Post Links': list(post_links)})

# Save to Excel
output_path = r'C:\Users\HP\OneDrive\İş masası\facebook_posts.xlsx'
df.to_excel(output_path, index=False)

print(f"Scraped {len(post_links)} post links. Saved to {output_path}")

# Close browser
driver.quit()
