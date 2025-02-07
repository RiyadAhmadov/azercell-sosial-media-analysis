import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

chrome_driver_path = "chromedriver.exe"
service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service)
driver.get("https://www.facebook.com/")

time.sleep(40)

pickle.dump(driver.get_cookies(), open("facebook_cookies.pkl", "wb"))

driver.quit()