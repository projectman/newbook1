
import time
from base.main_driver import MainDriver
from pages.home.login_page import LoginPage
from pages.models.models_page import ModelsPage


class HomePage(MainDriver):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.lp = LoginPage(self.driver)
        self.mp = ModelsPage(self.driver)

    ##############    Service Methods   #####################
    def checkLogoffHome(self):
        """
        It verifies that page logged out, if not -> Log out;
        Check it is no home page after previous verify, if not go home page.
        Returns nothing.
        """
        # Verify avatar and logout if available. Then Log out.
        if self.lp.avatarAvailableForClick():
            self.lp.waitClickAvatar()
            self.lp.waitClickLogout()

        # Verify if not on home page: go to home page.
        expected_url = self.data["url"]
        actual_url = self.getUrl()
        if not self.util.verifyTextMatch(expected_url, actual_url):
            self.mp.openHomePageWaitLogin()

    ##############     Main Methods     #####################
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
        result = [(element is not None)]
        self.elementClick("", "", element)

        # After click on page available test "Save Money,"
        result.append(self.isElementPresent(self.data["save_money"]))

        # Wait Central button "Sing Up" is available and click it.
        self.waitForClickElement(self.data["central_signup"], True)

        # On the opened frame there is text "Create a"
        result.append(self.isElementPresent(self.data["create_a"]))

        # Close the frame for create client
        elements_2 = self.waitAllElementsLocated(self.data["close_create"])
        self.elementClick("", "", elements_2[0])

        return self.util.absentFalseInList(result)

    def verifyForAgenciesElements(self):
        """
        Return True if all "For Agencies" elements are visible on the page.
        """

        # Find top element button "For Agencies" and click it
        element = self.getElement(self.data["for_agencies_top"])
        result = [(element is not None)]
        self.elementClick("", "", element)

        # Find the text on page:"Free up your" on the page
        result.append(self.isElementPresent(self.data["free_up"]))

        # Wait  button "Inquire" is available and click it.
        self.isElementDisplayed(self.data["inquire_btn"])

        # On the page still email field "Email"
        result.append(self.isElementPresent(self.data["email_fld"]))

        return self.util.absentFalseInList(result)

    def verifyForModelsElements(self):
        """
        Return True if all "For Models" elements are visible on the page.
        """
        # Visibility of Element "For Models" in the top menue
        element = self.getElement(self.data["for_models_top"])
        result = [(element is not None)]
        self.elementClick("", "", element)

        # After click on page available test "Take control" -> add True
        result.append(self.isElementDisplayed(self.data["take_control"]))

        # Find parent handle -> Main Window
        parent_window = self.findParentWindow()

        # Wait Central button "App Store" is available and click it.
        self.waitForClickElement(self.data["app_store"], True)

        # wait until EC.new_window_is_opened(current_handles)
        self.waitNewWindowOpen([parent_window])
        # Find all handles
        handles = self.findAllHandles()
        for handle in handles:
            if handle != parent_window:
                self.switchToWindow(handle)
                # On the opened window there must be text "Newbook" -> add True
                result.append(
                    self.waitElementLocated(
                        self.data["app_newbook"], "xpath", 15))
                time.sleep(5)
                # Close the window of App Store
                self.closeWindow()

        return self.util.absentFalseInList(result)


