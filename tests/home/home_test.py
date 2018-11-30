from utilities.statusdisplay import StatusDisplay
from pages.home.home_page import HomePage
from pages.home.login_page import LoginPage
from pages.models.models_page import ModelsPage
import pytest
import time

@pytest.mark.usefixtures("oneTimeSetUp")
class TestHome:

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.hp = HomePage(self.driver)
        self.ts = StatusDisplay(self.driver)
        self.lp = LoginPage(self.driver)
        self.mp = ModelsPage(self.driver)
        # logout first after log in.
        self.lp.waitClickAvatar()
        self.lp.waitClickLogout()
        # return to home Page
        self.mp.openHomePageWaitLogin()


    def test_elementsAvailable(self):
        """ Check all filter elements available on Home Page after log out.
        . TC # 027
        """

        # own verify method for Home page
        res = self.hp.verifyHomePageElements()

        self.ts.markFinal(
            "TC #027 All elements are available on Home page :",
            res, ": TC #027 TOTALLY FAILED test_elementsAvailable.")

    def test_verifyForClientsBtn(self):
        """ Check all elements available on Home Page after click "For Clients.
        . TC # 028
        """

        # own verify method for Home page
        res = self.hp.verifyForClientsElements()

        self.ts.markFinal(
            "TC #028 All elements available after click For Clients :",
            res, ": TC #028 TOTALLY FAILED test_verifyForClientsBtn.")