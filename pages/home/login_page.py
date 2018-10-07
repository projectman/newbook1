
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

    def newLogPage(self):
        """ print empty line in front of every new report. """
        str_el = "#"*10 + "  New LOG  " + 10*"#"
        self.specialLogLine(str_el)

    # Actions
    def clickLoginButton(self):
        self.elementClick(self._login_xpath)

    def enterEmail(self, email):
        self.sendKeys(email, self._email_xpath)

    def enterPassword(self, password):
        self.sendKeys(password, self._password_xpath)

    def clickSubmitButton(self):
        self.elementClick(self._submit_xpath)

    def login(self, email='', password=''):

        # Home page
        time.sleep(3)
        self.clickLoginButton()
        self.enterEmail(email)
        self.enterPassword(password)
        self.clickSubmitButton()

    def waitButtonAdvanced(self):
        self.waitForClickElement("//button/span[text()='Advanced Filters']")

    def verifyLoginSuccessful(self):
        return self.isElementPresent("//div[contains(text(),'Filter by Category')]")

    def verifyLoginFail(self):
        return self.isElementPresent("//div[text()=' Client Sign In ']")

    def verifyTitle(self, expectedTitle):
        """ Verify that tile after login as it should be. """
        # !!! update with selenium driver class !!!
        if expectedTitle in self.getTitle():
            return True
        else:
            return False

    def waitClickAvatar(self):
        # Wait found and click
        self.waitForClickElement("//div[@class='square-dummy']", True)

    def waitClickLogout(self):
        element = self.waitForClickElement("//div[@class='link link_type_logout link_active']")
        self.webScrollElement(element)
        self.elementClick("//div[@class='link link_type_logout link_active']")

    def waitConfirmLoggedout(self):
        return self.waitElementLocated("//div[text()=' Client Sign In ']")


    def verifyLogoutSuccessfull(self):
        self.waitClickAvatar()
        self.waitClickLogout()
        return self.waitConfirmLoggedout()



