from selenium import webdriver
import time
from pages.home.login_page import LoginPage
import unittest
import pytest

# import time

@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class LoginTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.lp = LoginPage(self.driver)

    @pytest.mark.run(order=2)
    def test_validLogin(self):
        """
        Test Login page with valid credentials.
        """
        self.lp.login('man4testing@gmail.com', 'New12345$')
        # Confirm login in
        time.sleep(2)
        # Debug print(driver.page_source)
        assert self.lp.verifyLoginSuccessful()
        time.sleep(3)
        self.driver.close()

    @pytest.mark.run(order=1)
    def test_invalidLogin(self):
        """Test Login with invalid login credentials. """
        self.lp.login('', '')
        # Confirm login in with empty credential
        time.sleep(2)
        assert self.lp.verifyLoginFail()
        time.sleep(2)
        # don't close driver. it needs on 2nd test

# ff = LoginTest()
# ff.valid_login()
