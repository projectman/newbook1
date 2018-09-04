from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Safari()
driver.get('https://stage1.fmny.mobi')
driver.maximize_window()

element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()=' Log In ']"))
    )
# print(dir(element))
element.click()

driver.quit()
