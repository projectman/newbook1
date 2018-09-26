
import time
from base.selenium_driver import SeleniumDriver


class LoginPage(SeleniumDriver):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver


    _login_xpath = "//button[text()=' Log In ']"
    _email_xpath = "//input[@placeholder='Enter E-mail address']"
    _password_xpath = "//input[@placeholder='Enter password']"
    _submit_xpath = "//button[text()=' Log In ']"


    # Actions
    def clickLoginButton(self):
        self.elementClick(self._login_xpath)

    def enterEmail(self, email):
        self.sendKeys(email, self._email_xpath)

    def enterPassword(self, password):
        self.sendKeys(password, self._password_xpath)

    def clickSubmitButton(self):
        self.elementClick(self._submit_xpath)

    def login(self, email, password):

        # Home page
        time.sleep(3)
        self.clickLoginButton()
        print("test print in LoginPage.login")
        # Login page
        self.enterEmail(email)
        self.enterPassword(password)
        self.clickSubmitButton()

    def verifyLoginSuccessful(self):
        return self.isElementPresent("//div[contains(text(),'Filter by Category')]")

    def verifyLoginFail(self):
        return self.isElementPresent("//div[text()=' Client Sign In ']")
