
import time
from base.basepage import BasePage
import json


class LoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # get dictionary with data testing from data.json
        self.data = json.load(open('utilities/data.json'))

    def get_data(self):
        """ Return dictionary with data for testing."""
        return self.data

    def newLogPage(self):
        """ print empty line in front of every new report. """
        str_el = "#"*20 + 10*" " +" NEW LOG " + 10*" " + 20*"#"

        self.specialLogLine(str_el+"; "+self.driver.title)

    # Actions
    ## Actions. Waits and Clicks
    def clickUpLoginButton(self):
        """ Wait Login UP-RIGHT button from Home page available
        then click it if 2nd argument is True."""
        self.waitForClickElement("//button[text()=' Log In ']", True)

    def clickSubmitButton(self):
        self.elementClick(self.data["signin_login_btn"])

    def waitSubmitButton(self):
        self.waitForClickElement(self.data["signin_login_btn"])

    def clickReLoginButton(self):
        self.waitForClickElement(self.data["up_login"], True)

    def waitButtonAdvanced(self):
        self.waitForClickElement("//button/span[text()='Advanced Filters']")

    def waitClickAvatar(self):
        # Wait found and click
        self.waitForClickElement("//div[@class='square-dummy']", True )

    def waitClickLogout(self):
        element = self.waitForClickElement("//div[@class='link link_type_logout link_active']")
        self.webScrollElement(element)
        self.elementClick("//div[@class='link link_type_logout link_active']")

    def getCurrentPageUrl(self):
        return self.getUrl()

    ## Actions. Enters.
    def enterEmail(self, email):
        self.sendKeys(email, self.data["email_field"])

    def enterPassword(self, password):
        self.sendKeys(password, self.data["pass_field"])

    def verifyLoginSuccessful(self):
        return self.isElementPresent("//div[contains(text()]")

    ### Verifications.
    def verifySigninText(self):
        # Verify that text "Client Sign In is available on page.
        return self.isElementDisplayed(self.data["signin_text"])

    def verifyTitle(self, expectedTitle):
        """ Verify that tile after login as it should be. """
        self.waitButtonAdvanced()  # make sure that page downloaded.
        return self.verifyPageTitle(expectedTitle)

    ########################### VERIFiCations  ##################################
    #                                                                           #
    def verifyFilterExists(self):
        """Verification that Filter button exists on the page. TC #003.1; #004.3
        Return True or False."""
        # Wait first element clickable.
        # As element has default locator XPATH, it abasement.

        return self.isElementDisplayed(self.data["filter_btn"])

    def verifyUrlHome(self):
        """ Verification that URL of "/browser" page is the requested for TC #003.2
        Return True or False."""
        return self.util.verifyTextContains(self.getUrl(), self.data["models_url"])

    def verifyAvatarExists(self):
        """ Verification that URL of "/browser" page is the requested for TC #003.3; TC #004.4
        Return True or False."""
        return self.isElementDisplayed(self.data["avatar_link"])

    def verifyLogoutSuccessfull(self):
        """ Click on avatar, move on Account Settings Page,
        Log out of your Account. Check URL ...mobi/browse. TC 004.1"""
        self.waitClickAvatar()
        self.waitClickLogout()
        return self.util.verifyTextContains(self.getUrl(),
                                            self.data["models_url"])

    def verifyLoginExists(self):
        """ Return True if link to "Log In" exists.TC 004.2; 002.4"""
        return self.isElementDisplayed(self.data["up_login_link"])   # Here need to be found <a href > with "Log In"

    def verifyBackBrowser(self):
        """ Click on BACK button in Browser.
        Verify Sign In text exists then return True. TC # 005.1"""
        self.driver.back()
        return self.verifySigninText()

    def verifyHomePage(self):
        """ Visit home page when user logoffed.
        Verify title "New book. TC 006.1 """
        self.driver.get(self.data["url"])
        return self.isElementDisplayed(self.data["nb_logo"])

    def verifyMadeBetter(self):
        """
        Visit home page when user logout verify title "New book. TC 006.2
        :return: True/False.
        """
        return self.isElementDisplayed(self.data["made_better"])

    def verifySingupModel(self):
        """
        Visit home page when user logout verify link "Sing Up as Model" TC 006.2
        :return: True/False.
        """
        return self.isElementPresent(self.data["signup_model"])

    def verifySignupPage(self):
        """
        Open singUp page and verify it. TC #002.1
        :return:   True if Client SignU on Sing Up page avaible.
        """
        self.clickReLoginButton()
        return self.verifySigninText()

    def verifyInvalidLoginFail(self):
        """Verify that wrong credentials doesn't allow
        to login the account.
        Return list of tuples (boolean PASS, user, pass)
        ,results of tests for every combination for
        all variants with boolean. TC # 007 """
        # 1. Need to be clicked on Login for for the beginning
        self.waitForClickElement(self.data["up_login_link"], True)

        result = []
        for item in self.data["wrong_cr"]:

            self.login(item["user"], item["pass"])
            self.waitSubmitButton()    # 007.1-16
            # Check that 1st element is available on page
            el_1 = self.isElementPresent(item["el_1"])
            # Check the 2nd element is available on page
            el_2 = self.isElementPresent(item["el_2"])
            result.append((el_1 and el_2, item["user"], item["pass"]))

        return result

    def verifyEmailAvailable(self):
        """
        Verify that email field available then return True. Other way false.
        """
        return self.isElementPresent(self.data["email_field"])

    def verifyPassAvailable(self):
        """
        Verify that password field available then return True. Other way false.
        """
        return self.isElementPresent(self.data["pass_field"])                 #
    #########################


    # "//div[text()='Password']/div[text()=' This field is required. ']"
    #  "//div[text()='E-mail Address']/div[text()=' This field is required. ']"

    # Logins
    def login(self, email='', password=''):
        # Home page
        self.enterEmail(email)
        self.enterPassword(password)
        self.clickSubmitButton()


