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
        Test Login page with valid credentials.
        """
        # self.lp.login( 'man4testing@gmail.com', 'New12345$' )
        # Confirm login in
        self.lp.waitButtonAdvanced() # make sure that page downloaded.

        # Verify that right title exists on the page.
        res_1 = self.lp.verifyTitle("Newbook")
        self.ts.mark(res_1, "Title Verification.")

        # Verify that wrong title doesn't exists on the page.
        res_2 = self.lp.verifyTitle("Newbook")
        self.ts.mark(res_2, "Wrong Title Verification.")

        # Debug print(driver.page_source)
        res_3 = self.lp.verifyLoginSuccessful()
        self.ts.markFinal(
            "Login frame testing: ", res_3, "Login Successful Verification.")

    def test_validLogout(self):
        """Test Login with invalid login credentials. """
        res = self.lp.verifyLogoutSuccessfull()
        self.ts.mark(res, "Logout Verification.")
        assert res

    def test_invalidLogin(self):

        # Confirm login in with wrong credential
        self.lp.relogin()
        res = self.lp.verifyLoginFail()
        self.ts.mark(res, "Failed wrong credentials verification.")
        assert res

# ff = LoginTest()
# ff.valid_login()
