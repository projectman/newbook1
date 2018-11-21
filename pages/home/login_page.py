
import time
from base.main_driver import MainDriver
import json


class LoginPage(MainDriver):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def get_data(self):
        """ Return dictionary with data JSON for testing."""
        return self.data

    def newLogPage(self):
        """ print empty line in front of every new report. """
        str_el = "#"*20 + 10*" " +" NEW LOG " + 10*" " + 20*"#"

        self.specialLogLine(str_el+"; "+self.driver.title)

    # Actions
    ## Actions. Waits and Clicks
    def clickUpLoginButton(self):
        """ Wait Login TOP-RIGHT button from Home page available
        then click it if 2nd argument is True."""
        self.waitForClickElement(self.data["up_login"], True)

    def clickSubmitButton(self):
        self.elementClick(self.data["signin_login_btn"])

    def existSubmitButton(self):
        """
        Return True if the central submit button "Log In" on Sign In page exists
        """
        return self.isElementPresent(self.data["signin_login_btn"])

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

    def waitAndConfirmElementLocated(self, locator, locator_type="xpath"):
        """Wait until element can be located,
        return: True if element was located after explicit waiting."""
        found = self.waitElementLocated(locator, locator_type)   #!!! Refact
        if found is not None:
            return True
        else:
            return False

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
        """Verification that Filter button exists on the page.
        TC #003.1; #004.3
        Return True if filter exists and Flase if doesn't exist. ."""
        # Wait first element clickable.
        # As element has default locator XPATH, it abasement.

        return self.isElementDisplayed(self.data["filter_btn"])

    def verifyUrlHome(self):
        """ Verification that URL of "/browser" page is the requested for TC #003.2
        Return True or False."""
        return self.util.verifyTextContains(self.getUrl(), self.data["models_url"])

    def verifyAvatarExists(self):
        """ Verification that URL of "/browser" page is the requested for
        TC #003.3; TC #004.4
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
        return self.isElementDisplayed(self.data["text_top_local"])

    def verifySingupModel(self):
        """
        Visit home page when user logout verify link "Sing Up as Model" TC 006.2
        :return: True/False.
        """
        return self.isElementPresent(self.data["signup_topright"])

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
        counter = 7
        for item in self.data["wrong_cr"]:

            self.login(item["user"], item["pass"])
            # 007.1-016.1
            # if we don't find the button, as logged in- no reasons to wait.
            # !!! create service method for braking loops when elment is not
            # exists in loop with logs.

            out = False
            if not self.existSubmitButton():
                break
            # Check that 1st element is available on page; # 007.2 - 017.2
            if self.waitAndConfirmElementLocated(item["el_1"]):
                # Check the 2nd element is available on page
                if self.isElementDisplayed(item["el_2"]):
                    out = True
            else:
                out = False
            # ??? add in future control text in the text field  !!!
            # Check that 1st element is available on page; # 007.3cata - 017.3
            result.append((out, item["user"], item["pass"]))
            time.sleep(2)    # For visual debugging. !!! delete

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

    def login(self, email='', password=''):
        """
        Action on Sign IN page for sign in.
        """
        self.enterEmail(email)
        self.enterPassword(password)
        self.clickSubmitButton()
