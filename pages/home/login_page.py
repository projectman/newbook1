
import time
from base.main_driver import MainDriver
import json


class LoginPage(MainDriver):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Actions
    ## Actions. Waiters and Clicks
    def waitAndClickUpLoginButton(self):
        """ Wait Login TOP-RIGHT button from Home page available
        then click it if 2nd argument is True."""
        self.waitForClickElement(self.data["up_login"], True)

    def clickSubmitButton(self):
        self.elementClick(self.data["signin_login_btn"])

    def existSubmitButton(self):
        # Return True if the central submit button "Log In"
        # on Sign In page exists
        return self.isElementDisplayed(self.data["signin_login_btn"])

    def waitButtonAdvanced(self):
        # Wait until button "Advanced Filters" available for click
        self.waitForClickElement(self.data["advanced_filters"])

    def waitAvatarAndClick(self):
        # Wait Avatar area and click it. Return True if Avatar was found.
        self.waitForClickElement(self.data["avatar_square"], True)


    def isAvatarExists(self):
        """
        Return True if avatar is available for click.
        """
        return self.isElementDisplayed(self.data["avatar_square"])

    def waitClickLogout(self):
        # Wait element button "Log off" available for click and click it
        # after scroll to it.
        element = self.waitForClickElement(self.data["logout_btn"])
        self.webScrollElement(element)
        # After scroll the object of element may changed. Need recall again.
        self.elementClick(self.data["logout_btn"])

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

    ## Actions. Entries.
    def enterEmail(self, email):
        self.sendKeys(email, self.data["email_field"])

    def enterPassword(self, password):
        self.sendKeys(password, self.data["pass_field"])


    ### Verifications.

    def isUrlModelsBrowse(self):
        """
        Return True if current URL of web is equal self.data["models_url"]
        """
        expected_url = self.data["models_url"]
        actual_url = self.getUrl()

        return self.util.verifyTextMatch(expected_url, actual_url)

    def verifySigninText(self):
        # Verify that text "Client Sign In is available on page.
        return self.isElementDisplayed(self.data["signin_text"])

    def verifyEmailAvailable(self):
        # Verify that email field available then return True. Other way false.
        return self.isElementDisplayed(self.data["email_field"])

    def verifyPassAvailable(self):
        # Verify that password field available then return True. Other: false.
        return self.isElementDisplayed(self.data["pass_field"])

    def avatarAvailableForClick(self):
        """
        Return avatar link element after waiting it is available for clicking.
        """
        return self.isElementClickable(
                                    self.getElement(self.data["avatar_link"]))

    ########################### VERIFiCations  #################################
    #                                                                          #
    def verifyFilterExists(self):
        """Verification that Filter button exists on the page.
        TC #003.1; #004.3
        Return True if filter exists and Flase if doesn't exist. ."""
        # Wait first element clickable.
        # As element has default locator XPATH, it abasement.
        return self.isElementDisplayed(self.data["filter_btn"])

    def avatarDoesExists(self):
        """ Verification that URL of "/browser" page is the requested for
        TC #003.3; TC #004.4
        Return True or False."""
        return self.isElementDisplayed(self.data["avatar_link"])

    def isLogoutSuccessfull(self):
        # return True if logout is successful.
        return not self.avatarDoesExists()

    def isUpLoginExists(self):
        # Return True if link to "Log In" exists.TC 004.2; 002.4
        return self.isElementDisplayed(self.data["up_login_link"])

    def verifyBackBrowser(self):
        """ Click on BACK button in Browser.
        Verify Sign In text exists then return True. TC # 005.1"""
        self.pushBrowserBackBtn()
        return self.verifySigninText()

    def verifyHomePage(self):
        """ Visit home page when user logoffed.
        Verify title "New book. TC 006.1 """
        # As it first method in test case we need to confirm that
        # we're logoffed and then only open home page (data["url"])
        if not self.isLogoutSuccessfull():
            self.logout()

        self.openUrlPage(self.data["url"])
        return self.isElementDisplayed(self.data["nb_logo"])

    def verifyMadeBetter(self):
        """
        Visit home page when user logout verify title "New book. TC 006.2
        :return: True/False.
        """
        self.util.sleep(6)
        return self.isElementDisplayed(self.data["text_top_local"])

    def verifySingupModel(self):
        """
        Visit home page when user logout verify link "Sing Up as Model" TC 006.2
        :return: True/False.
        """
        return self.isElementDisplayed(self.data["signup_topright"])

    def verifySignupPage(self):
        """
        Open singUp page and verify it. TC #002.1
        :return:   True if Client SignU on Sing Up page avaible.
        """
        self.waitAndClickUpLoginButton()
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
            # Check 1st element of UI is available on page; # 007.2 - 017.2
            if self.waitAndConfirmElementLocated(item["el_1"]):
                # Check the 2nd element of UI is available on page
                if self.isElementDisplayed(item["el_2"]):
                    out = True
            else:
                out = False
            # ??? add in future control text in the text field  !!!
            # Check that 1st element is available on page; # 007.3cata - 017.3
            result.append((out, item["user"], item["pass"]))
            time.sleep(2)    # For visual debugging. !!! delete

        return result

    def logout(self):
        """ Click on avatar, move on Account Settings Page,
        Log out of your Account. Check URL ...mobi/browse. TC 004.1"""
        self.waitAvatarAndClick()
        self.waitClickLogout()

    def login(self, email='', password=''):
        """
        Action on Sign IN page for sign in.
        """
        self.enterEmail(email)
        self.enterPassword(password)
        self.clickSubmitButton()
