from utilities.statusdisplay import StatusDisplay
from pages.home.login_page import LoginPage
import unittest
import pytest
import time

# import time
@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class LoginTest(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.lp = LoginPage(self.driver)
        self.ts = StatusDisplay(self.driver)

    @pytest.mark.run(order=1)
    def test_validLogin(self):
        """
        Test Login page with valid credentials.
        """
        # self.lp.login( 'man4testing@gmail.com', 'New12345$' )
        # Confirm login in
        print("title:", self.lp.driver.title)
        self.lp.waitButtonAdvanced() # make sure that page downloaded.

        # Verify that right title exists on the page.
        res_1 = self.lp.verifyTitle("Newbook")
        self.ts.mark(res_1, "Title Verification.")
        time.sleep(1)

        # Verify that wrong title doesn't exists on the page.
        res_2 = self.lp.verifyTitle("Newbook")
        self.ts.mark(res_2, "Wrong Title Verification.")
        time.sleep(1)

        # Debug print(driver.page_source)
        res_3 = self.lp.verifyLoginSuccessful()
        self.ts.markFinal(
            "Login frame testing: ", res_3, "Login Successful Verification.")
        time.sleep(1)


    @pytest.mark.run(order=2)
    def test_validLogout(self):
        """Test Login with invalid login credentials. """
        res = self.lp.verifyLogoutSuccessfull()
        print("res:", res)
        self.ts.mark( res, "Logout Verification." )
"""
    @pytest.mark.run(order=3)
    def test_invalidLogin(self):
        
        self.lp.login('', '')
        # Confirm login in with wrong credential
        time.sleep(2)
        res_1 = self.lp.verifyLoginFail()
        self.ts.mark(res_1, "Invalid login verification.")
        time.sleep(1)
        self.driver.close()

"""

# ff = LoginTest()
# ff.valid_login()
