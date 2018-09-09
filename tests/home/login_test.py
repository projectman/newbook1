from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pages.home.login_page import LoginPage
import unittest

# import time

class LoginTest(unittest.TestCase):

    def test_validLogin(self):
        """
        Test Login page.
        """
        home_url = 'https://stage1.fmny.mobi'
        driver = webdriver.Firefox()
        driver.get(home_url)
        driver.implicitly_wait(5)
        print ("test before LoginPage")

        lp = LoginPage(driver)
        lp.login('man4testing@gmail.com', 'New12345$')

        # Confirm login in
        time.sleep(5)
        # Debug print(driver.page_source)
        if "Search by models’ name" in driver.page_source:
            print("Login successful, found: ", 'Search by models’ name')
        else:
            print("Login failed.")

        time.sleep(5)
        driver.close()

if __name__ == '__main__':
    unittest.main(verbosity=2)

# ff = LoginTest()
# ff.valid_login()
