
import time
from base.basepage import BasePage


class LoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver


    _login_xpath = "//button[text()=' Log In ']"
    _email_xpath = "//input[@placeholder='Enter E-mail address']"
    _password_xpath = "//input[@placeholder='Enter password']"

    def newLogPage(self):
        """ print empty line in front of every new report. """
        str_el = "#"*20 + 10*" " +" NEW LOG " + 10*" " + 20*"#"
        self.specialLogLine(str_el)

    # Actions
    ## Actions. Waits and Clicks
    def clickLoginButton(self):
        """ Wait Login button from Home page available
        then ckick it if 2nd argument is True."""
        self.waitForClickElement("//button[text()=' Log In ']", True)

    def clickSubmitButton(self):
        self.elementClick(self._login_xpath)

    def waitSubitButton(self):
        self.waitForClickElement(self._login_xpath)

    def clickReLoginButton(self):
        self.waitForClickElement("//a[text()='Log In']", True)

    def waitButtonAdvanced(self):
        self.waitForClickElement("//button/span[text()='Advanced Filters']")

    def waitClickAvatar(self):
        # Wait found and click
        self.waitForClickElement( "//div[@class='square-dummy']", True )

    def waitClickLogout(self):
        element = self.waitForClickElement( "//div[@class='link link_type_logout link_active']" )
        self.webScrollElement( element )
        self.elementClick( "//div[@class='link link_type_logout link_active']")

    def waitConfirmLoggedout(self):
        return self.waitElementLocated( "//a[text()='Log In']" )

    ## Actions. Enters.
    def enterEmail(self, email):
        self.sendKeys(email, self._email_xpath)

    def enterPassword(self, password):
        self.sendKeys(password, self._password_xpath)

    def verifyLoginSuccessful(self):
        return self.isElementPresent( "//div[contains(text(),'Filter by Category')]" )

    ### Actions. Verifications.
    def verifyTitle(self, expectedTitle):
        """ Verify that tile after login as it should be. """
        return self.verifyPageTitle(expectedTitle)

    def verifyLogoutSuccessfull(self):
        self.waitClickAvatar()
        self.waitClickLogout()
        return self.waitConfirmLoggedout()

    def verifyLoginFail(self):
        self.waitElementLocated("//div[text()=' This field is required. ']")
        return self.isElementPresent("//div[text()=' This field is required. ']")

    # Logins
    def login(self, email='', password=''):
        # Home page

        self.clickLoginButton()
        self.enterEmail( email )
        self.enterPassword( password )
        self.clickSubmitButton()

    def relogin(self, email='', password=''):
        self.clickReLoginButton()
        self.waitSubitButton()
        self.enterEmail(email)
        self.enterPassword(password)
        self.clickSubmitButton()
