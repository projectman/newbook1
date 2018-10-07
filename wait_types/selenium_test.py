from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

import time

driver = webdriver.Firefox()
driver.get('https://stage1.fmny.mobi')

# Home page
wait = WebDriverWait(driver, 10, 0.5)
wait.until(EC.element_to_be_clickable(((By.XPATH, "//button[text()=' Log In ']")))).click()

# Login frame
driver.find_element(By.XPATH, "//input[@placeholder='Enter E-mail address']").\
    send_keys('man4testing@gmail.com')
driver.find_element(By.XPATH, "//input[@placeholder='Enter password']").\
    send_keys('New12345$')
driver.find_element( By.XPATH, "//button[text()=' Log In ']" ).click()

# Catalogue page
avatar = wait.until(EC.element_to_be_clickable(((
    By.XPATH, "//div[@class='square-dummy']"))))
avatar.click()

# Profile page
logout_btn = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//div[@class='link link_type_logout link_active']")))
driver.execute_script("arguments[0].scrollIntoView(true);", logout_btn)
logout_btn.click()

# Client Sing In page Verification
client_signin = wait.until(
    EC.presence_of_element_located((
        By.XPATH, "//div[text()=' Client Sign In ']")))

if client_signin is not None:
    print("logout_btn is found")
time.sleep(3)
#driver.quit()
