import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

# Path to your ChromeDriver
chrome_driver_path = r"C:\Users\HP\OneDrive\İş masası\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path)

# Open browser
driver = webdriver.Chrome(service=service)
driver.get("https://www.facebook.com/")

time.sleep(40)

# Save cookies after logging in
pickle.dump(driver.get_cookies(), open("facebook_cookies.pkl", "wb"))

print("Cookies saved successfully!")
driver.quit()



# import pickle
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# import time


# # Path to ChromeDriver
# chrome_driver_path = r"C:\Users\HP\OneDrive\İş masası\chromedriver-win64\chromedriver.exe"
# service = Service(chrome_driver_path)

# # Start driver
# driver = webdriver.Chrome(service=service)
# driver.get("https://www.facebook.com/")


# time.sleep(50)

# # Load saved cookies
# cookies = pickle.load(open("facebook_cookies.pkl", "rb"))
# for cookie in cookies:
#     driver.add_cookie(cookie)

# # Refresh to apply cookies
# driver.refresh()

# print("Logged in using cookies!")