import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class LoginPage():

    def __init__(self, driver):
        self.driver = driver

    def login(self, email, password):
        print("Login in def login")
        # Home page
        time.sleep(5)
        element = self.driver.find_element(
            By.XPATH, "//button[@type='submit']")
        element.click()

        # Move to page Login
        # Act on Login page
        email_el = self.driver.find_element(By.XPATH,
                                        "//input[@placeholder='Enter E-mail address']")
        email_el.send_keys(email)

        pwrd_el = self.driver.find_element(By.XPATH,
                                       "//input[@placeholder='Enter password']")
        pwrd_el.send_keys(password)

        login_btn = self.driver.find_element(By.XPATH,
                                         "//button[text()=' Log In ']")
        login_btn.click()