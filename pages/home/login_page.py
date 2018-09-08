import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class LoginPage():

    def __init__(self, driver):
        self.driver = driver


    _login_xpath = "//button[text()=' Log In ']"
    _email_xpath = "//input[@placeholder='Enter E-mail address']"
    _password_xpath = "//input[@placeholder='Enter password']"
    _submit_xpath = "//button[text()=' Log In ']"

    # Locators
    def getLoginButton(self):
        return self.driver.find_element(By.XPATH, self._login_xpath)

    def getEmailField(self):
        return self.driver.find_element(By.XPATH, self._email_xpath)

    def getPasswordField(self):
        return self.driver.find_element(By.XPATH, self._password_xpath)

    def getSubmitButton(self):
        return self.driver.find_element(By.XPATH, self._submit_xpath)

    # Actions
    def clickLoginBtn(self):
        self.getLoginButton().click()

    def enterEmail(self, email):
        self.getEmailField().send_keys(email)

    def enterPassword(self, password):
        self.getPasswordField().send_keys(password)

    def clickSubmitBtn(self):
        self.getSubmitButton().click()

    def login(self, email, password):
        # Home page
        time.sleep(3)
        self.clickLoginBtn()

        # Login page
        self.enterEmail(email)
        self.enterPassword(password)
        self.clickSubmitBtn()