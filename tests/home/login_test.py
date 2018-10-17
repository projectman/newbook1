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
        # Confirm login made for conftest.py
        # Verify that right title exists on the page.
        res_1 = self.lp.verifyTitle("Newbook")
        self.ts.mark(res_1, "Title Verification SUCCESS.")

        # Verify that wrong title doesn't exists on the page.
        res_2 = self.lp.verifyTitle("Nebook")
        self.ts.mark(res_2, "Wrong Title Verification SUCCESS.")

        # Debug print(driver.page_source)
        res_3 = self.lp.verifyLoginSuccessful()
        self.ts.markFinal(
            "Login frame testing: ", res_3,
            "Right credentials Login SUCCESS.")
        assert res_3

    def test_validLogout(self):
        """Test Login with invalid login credentials. """
        res = self.lp.verifyLogoutSuccessfull()
        self.ts.mark(res, "Logout Verification SUCCESS.")
        assert res

    def test_invalidLoginEmpty(self):

        # Confirm login in with wrong credential
        res = self.lp.verifyInvalidLoginFail()
        self.ts.mark(res, "Wrong credentials DON'T PASS.")
        assert res

# ff = LoginTest()
# ff.valid_login()
