
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


        return self.util.absentFalseInList(result)

    def verifyForClientsElements(self):
        """
        Return True if all 3 elements are visible on the page.
        """

        # Visibility of Element "For Clients" in the top menue
        element = self.getElement(self.data["for_client_top"])
        if element is not None:
            result = [True]
        else:
            result = [False]
        self.elementClick("", "", element)

        # After click on page available test "Save Money,"

        result.append(self.isElementPresent(self.data["save_money"]))

        # Wait Central button "Sing Up" is available and click it.
        self.waitForClickElement(self.data["central_signup"], True)

        # On the opened fraim there is text "Create a"
        result.append(self.isElementPresent(self.data["create_a"]))

        # Close the frame for create client
        self.elementClick("", "", self.getElementList(
                                self.data["close_create"])[0]
                          )

        return self.util.absentFalseInList(result)
