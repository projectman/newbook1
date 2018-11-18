from utilities.statusdisplay import StatusDisplay
from pages.home.login_page import LoginPage
import pytest
import time

# import time
@pytest.mark.usefixtures("oneTimeSetUp")
class TestLogin():

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.lp = LoginPage(self.driver)
        self.ts = StatusDisplay(self.driver)

    def test_validLogin(self):
        """
        FM1118-003 Test Models page after valid credentials.
        """
        # Text "Filter by Category" exists; TC #003.1
        res_1 = self.lp.verifyFilterExists()
        self.ts.mark(res_1, "#003.1: Login verification.")

        # Page url is http://stage1.fmny.mobi/browse; TC #003.2
        res_2 = self.lp.verifyUrlHome()
        self.ts.mark(res_2, "#003.2: Home pages URL verification.")

        # Avatar of user exists; TC #003.3
        res_3 = self.lp.verifyAvatarExists()
        self.ts.mark(res_3, "#003.3 Avatar availability verification.")

        # Final confirmation for Test Case.
        final = res_1 and res_2 and res_3
        self.ts.markFinal(
            "TC #003: Test Models page after log in with valid credentials: ", final,
            ": TC #003 TOTALLY FAILED.")

    def test_validLogout(self):
        """Test Login out from the site. TC004"""
        res_1  = self.lp.verifyLogoutSuccessfull() #  004.1
        self.ts.mark(res_1, "#004.1: URL after logout as expected.")

        res_2 = self.lp.verifyLoginExists() #  004.2
        self.ts.mark(res_2, "#004.2: Log In link exists.")

        res_3 = not self.lp.verifyFilterExists() #  004.3
        self.ts.mark(res_3, "#004.3: Button Filter must not exist.")

        res_4 = not self.lp.verifyAvatarExists()  # 004.4
        self.ts.mark(res_4, "Avatar must not exist.")

        # Final confirmation for Test Case.
        final = res_1 and res_2 and res_3 and res_4
        self.ts.markFinal(
            "TC #004: Test Models page after log off successful: ", final,
            ": TC #004 TOTALLY FAILED.")

    def test_backBrowser(self):
        """Go "Back" in browser, after Log out. TC #005
        Site must open Sign Up page. User still logged out.
        """
        res_1 = self.lp.verifyBackBrowser()  # Click "BACK" and verify TC # 005.1
        self.ts.mark(res_1, "#005.1: BACK button pushed.")

        # Functionality not available. No reason to implement all tests.
        final = res_1 # and res_2 and res_3 and res_4
        self.ts.markFinal(
            "TC #005: Push BACK button on browser with Logoffed user: ", final,
            ": TC #005 TOTALLY FAILED.")

    def test_homePageLogoffed (self):
        """Visit "Home page", after log out. TC #006, 001"""
        res_1 = self.lp.verifyHomePage()  # # 006.1
        self.ts.mark(res_1, "#006.1: Visit to Home Page: Logo exists")

        res_2 = self.lp.verifyMadeBetter()  # # 006.2
        self.ts.mark(res_2, "#006.2: Visit to Home Page: 'Making better' exists ")

        res_3 = self.lp.verifySingupModel()  # # 006.3
        self.ts.mark(res_3, "#006.3: Visit to Home Page: 'Sign Up as a model' exists")

        final = res_1  and res_2 and res_3
        self.ts.markFinal(
            "TC #006 & 001: Visit on Home Page with Logoffed user: ", final ,
            ": TC #006 TOTALLY FAILED.")


    def test_signupPage (self):
        """Sign in page elememts availability; . TC #002"""
        res_1 = self.lp.verifySignupPage()  # # 002.1
        self.ts.mark(res_1,
                     "#002.1: Visit to SignIn Page: 'Client Sign In' exists ")

        res_2 = self.lp.verifyEmailAvailable()  # # 002.2
        self.ts.mark(res_2,
                     "#002.2: Visit to SignIn Page: E-mail field is available.")

        res_3 = self.lp.verifyPassAvailable()  # # 002.3
        self.ts.mark(
            res_3,
            "#002.3: Visit to SignIn Page: Password field is available? ")

        res_4 = self.lp.verifyLoginExists()  # # 002.4
        self.ts.mark(res_4,
                     "#002.4: Visit to SignIn Page: E-mail field available? ")

        final = res_1 and res_2 and res_3 and res_4
        self.ts.markFinal(
            "TC #002: Visit on SingIn Page with Logoffed user:", final,
            ": TC #002 TOTALLY FAILED.")

    def test_invalidLogin(self):
        # Confirm login in with wrong credentials. TC # 007
        # For the first step we need move from the
        final = self.lp.verifyInvalidLoginFail()

        # Check if any items in list:
        if len(final) > 0:
            for result in final:
                print("inside loop test_invalidLogin:", result)
                self.ts.mark(result[0], ("TC 007 with "+str(result[1])+", "+str(result[2])
                             +"result:"))
            self.ts.markFinal(
                "TC #007: Login with invalid credentials impossible? ", final,
                ": TC #007 TOTALLY FAILED.")
        else:
            self.ts.markFinal(
                "TC #007: WRONG PROCESS: No results of invalid login tries :",
                None, ": TC #007 TOTALLY FAILED.")

# ff = LoginTest()
# ff.valid_login()
