
import time
from base.main_driver import MainDriver


class HomePage(MainDriver):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def verifyHomePageElements(self):
        """ It return TRue if all elements that need to be verified are
        available on Home page. """


        elements = self.data["hp_elements"]
        result =[]
        for element in elements:
            result.append(self.isElementPresent(element))

        time.sleep(5)

        return self.util.absentFalseInList(result)
