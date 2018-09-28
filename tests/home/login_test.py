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

    @pytest.mark.run(order=2)
    def test_validLogin(self):
        """
        Test Login page with valid credentials.
        """
        self.lp.login( 'man4testing@gmail.com', 'New12345$' )
        # Confirm login in
        time.sleep(1)
        res_1 = self.lp.verifyTitle()
        self.ts.mark(res_1, "Title Verified")
        # Debug print(driver.page_source)
        res_2 = self.lp.verifyLoginSuccessful()
        self.ts.mark(res_2, "Login Successful!")
        time.sleep(1)
        self.driver.close()

    @pytest.mark.run(order=1)
    def test_invalidLogin(self):
        """Test Login with invalid login credentials. """
        self.lp.login('', '')
        # Confirm login in with empty credential
        time.sleep(2)
        res_1 = self.lp.verifyLoginFail()
        self.ts.markFinal(res_1, "Test verifyed")
        time.sleep(1)
        # don't close driver. it needs on 2nd test

# ff = LoginTest()
# ff.valid_login()
