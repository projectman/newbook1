from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import utilities.custom_logger as cl
from utilities.util import Util
import json
import logging


class MainDriver():

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver
        self.util = Util()

        # get dictionary with data testing from data.json
        self.data = json.load(open('utilities/data.json'))

    def specialLogLine(self, message):
        """Any service announcement line for the new log."""
        self.log.debug(message)

    def openUrlPage(self, url):
        """
        Open the page with url address. Return nothing.
        """
        self.driver.get(url)
        is_opened = self.waitUrlMatchesExpected(url)

        if is_opened:
            self.log.debug("Opened the page with url: " + url)
        else:
            self.log.error("CAN NOT open the page with url: " + url)

    def getUrl(self):
        url = self.driver.current_url
        self.log.debug("Current page URL from getUrl method is "+url)
        return url

    def pushBrowserBackBtn(self):
        # Push "Back" button on browser;
        self.driver.back()
        # !!! add waiter that url is actual.
        self.log.debug("Button 'Back' was pushed on browser.")

    def getTitle(self):
        title = self.driver.title
        self.log("It got title of the page: " + title)
        return title

    def getByType(self, locator_type):
        locator_type = locator_type.lower()
        if locator_type == "id":
            return By.ID
        elif locator_type == "name":
            return By.NAME
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "css":
            return By.CSS_SELECTOR
        elif locator_type == "class":
            return By.CLASS_NAME
        elif locator_type == "link":
            return By.LINK_TEXT
        else:
            self.log.error("Locator type " + locator_type +
                          " not correct/supported")
        return False

    def getElement(self, locator, locator_type="xpath"):
        element = None
        try:
            locator_type = locator_type.lower()
            byType = self.getByType(locator_type)
            element = self.driver.find_element(byType, locator)
            self.log.debug("Element Found in getElement with locator: " + locator +
                          " and  locator_type: " + locator_type)
        except:
            self.log.error("Element NOT found in getElement with locator: " + locator +
                  " and  locator_type: " + locator_type)
        return element

    def getElementList(self, locator, locator_type='xpath'):
        """Get list of elements with given locator."""
        result = []
        try:
            locator_type = locator_type.lower()
            byType = self.getByType(locator_type)
            result = self.driver.find_elements(byType, locator)
            self.log.debug( "Element List with length: " +str(len(result)) +
                        "; Found with locator: " + locator +
                       " and  locator_type: " + locator_type )
        except:
            self.log.error( "Element LIST not Found with locator: " + locator +
                           " and  locator_type: " + locator_type )
        return result

    def elementClick(self, locator, locator_type="xpath", element=None):
        """
        Either provide element or a combination of locator and locator_type
        Return True if element found and clicked; Opposite return False
        """
        result = False
        try:
            if locator != "":
                new_element = self.getElement(locator, locator_type)
                new_element.click()
                self.log.debug("Clicked on element with locator: " + locator +
                          " locator_type: " + locator_type)
                result = True
            elif element is not None:
                self.log.debug(("Clicked on received element: " + str(element)))
                element.click()
                result = True
            else:
                self.log.error(("Can NOT click element as NO locator: "
                                + locator +
                                ", and NO element: " + str(element)))
        except:
            self.log.error("Cannot click on the element with locator: " +
                          locator + " locator_type: " + locator_type +
                           " or element :: " + str(element))
            # print_stack()
        return result

    def verifyPageIncludesText(self, expected_text):
        """
        Return: True if page include the 'expectedText. In other case: False.
        """
        try:
            actualText = self.driver.page_source
            if expected_text in actualText:
                result = True
                self.log.debug(
                    "Does current page includes text: " + str(expected_text)
                          + ": " + str(result))
            else:
                result = False
                self.log.error(
                    "Current page DOES NOT include text: '" + str(expected_text)
                    + "': " + str(result))
        except:
            result = False
            self.log.error(
                "Process FAILTURE: current page includes text: "
                + str(expected_text)
                + ": " + str(result))

        return result

    def verifyPageTitle(self, title_to_verify):
        """
        Verify the page Title
        Parameters:
        titleToVerify: Title on the page that needs to be verified
        """
        try:
            actualTitle = self.getTitle()
            return self.util.actualTextContainsExpected(actualTitle, title_to_verify)
        except:
            self.log.error("Failed to get page title")
            print_stack()
            return False

    def sendKeys(self, data, locator, locator_type="xpath"):
        """
        Send keys to an element
        Either provide element or a combination of locator and locator_type
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.getElement(locator, locator_type)
                element.clear()
                element.send_keys(data)
                self.log.debug("Sent data '" + data + "' to element with locator: "
                           + locator +
                           " locator_type: " + locator_type)
        except:
            self.log.error("Cannot send data '" + data + "' to element with locator: "
                           + locator +
                           " locator_type: " + locator_type)
            # print_stack()

    # !!! ???? If need method for if the location is for clickable element - use this
    # method again.
    def isElementClickable(self, element=None):
        """
        Return True if element from argument is clickable.
        In ther case return False of None if element in arguments doesn't exist.
        """
        # print ("methods of element: ", dir(element))
        try:
            if element.is_clickable:
                self.log.debug(("Element : " +
                              str(element) + " is clickable."))
                return True
            else:
                self.log.error(("Element : " +
                              str(element) + " is NOT clickable."))
                return False
        except:
            self.log.error(("Element DOES NOT clickable: " + str(element)))
            return False

    def getText(self, element, locator="", locator_type="xpath", info="No additional info."):
        """
        Get 'Text' on an element
        Either provide element or a combination of locator and locator_type
        """
        try:
            if element is None:  # This means if element is empty
                self.log.debug( "In locator condition: " + str(element) )
                element = self.getElement(locator, locator_type )
                self.log.debug("Before finding text")
            text = element.text
            self.log.debug("After finding element, size of text is: " + str(len(text)))
            if len( text ) == 0:
                text = element.get_attribute( "innerText" )
            if len( text ) != 0:
                self.log.debug(("Getting text on element :: " + str(text) + info))
                text = text
        except:
            self.log.error( "Failed to get text on element " + str(element)
                            + "; " + info)
            # print_stack()
            text = None
        return text

    def isElementDisplayed(self, locator="", locator_type="xpath", element=None):
        """
        Check if element is displayed
        Either provide element or a combination of locator and locator_type
        """
        try:
            if locator != "":  # This means if locator is not empty
                element = self.getElement( locator, locator_type )
            if element is not None:
                self.log.debug( "Element is displayed with locator: "
                               + locator + " locator_type: " + locator_type )
                return True
            else:
                self.log.error(
                    "Element not displayed with locator: " + locator +
                               " locator_type: " + locator_type )
                return False
        except:
            print( "Element not found" )
            return False

    def waitForClickElement(self, locator, click=False, locator_type="xpath",
                               timeout=5, pollFrequency=0.5):
        """Wait Element with locator, and click after found if True.
        :return: element
        """
        element = None
        try:
            byType = self.getByType(locator_type)
            self.log.debug("Waiting for maximum :: " + str(timeout) +
                  " :: seconds for element '" + locator + "' to be clickable")
            wait = WebDriverWait(self.driver, timeout, pollFrequency
                                 )
            element = wait.until(EC.element_to_be_clickable((byType, locator)))
            self.log.debug("Element '" + locator + "' appeared " + locator + " on the web page")
            if click:
                element.click()
                self.log.debug("Element '" + locator + "' clicked with locator " + locator + " on the web page")
        except:
            self.log.error("Element '" + locator + "' NOT appeared " + locator + " on the web page")
            # print_stack()
        return element

    def waitElementLocated(self, locator, locator_type="xpath",
                               timeout=5, pollFrequency=0.5):
        """Wait until Element will be present with locator. Return element. """
        element = None
        try:
            byType = self.getByType(locator_type)
            self.log.debug("Waiting for maximum :: " + str(timeout) +
                  " :: seconds for element to be LOCATED")
            wait = WebDriverWait(self.driver, timeout, pollFrequency)
            element = wait.until(EC.presence_of_element_located((
                byType, locator)))
            self.log.debug("Confirmed presence of element located with locator: "
                          + locator + " on the web page")
        except:
            self.log.error("NOT Confirmed presence of element with locator: "
                           + locator + " on the web page")
            # print_stack()
        return element

    def waitElementVisible(self, locator, locator_type="xpath",
                               timeout=5, pollFrequency=0.5):
        """Wait until Element will be visible with locator. Return element. """
        element = None
        try:
            byType = self.getByType(locator_type)
            self.log.debug("Waiting for maximum :: " + str(timeout) +
                  " :: seconds for element to be VISIBLE")
            wait = WebDriverWait(self.driver, timeout, pollFrequency)
            element = wait.until(EC.visibility_of_element_located((
                byType, locator)))
            self.log.debug("Confirmed VISIBILITY of element with locator: "
                          + locator + " on the web page")
        except:
            self.log.error("NOT Confirmed VISIBILITY of element with locator: "
                           + locator + " on the web page")
            # print_stack()
        return element

    def waitAllElementsLocated(self, locator, locator_type="xpath", timeout=5,
                               pollFrequency=0.5):
        """
        Wait untli all elements with locator will be present on the page.
        then return list of elements. In other case return empty list.
        """
        result = []
        try:
            byType = self.getByType(locator_type)
            self.log.debug(("Waiting for maximum :: "
                           + str(timeout) +
             " :: seconds for All elements Located with LOCATOR: " + locator))
            wait = WebDriverWait(self.driver, timeout, pollFrequency)
            result = wait.until(EC.presence_of_all_elements_located((
                byType, locator)))
            self.log.debug(
                ("Confirmed presence of ALL " + str(len(result))
                 + " elements located with locator: "
                 + locator + ", " + locator_type + " on the web page"))

        except:
            self.log.error(
                ("NOT Confirmed presence of ALL elements with locator: "
                           + locator + " on the web page"))

        return result

    def waitNewWindowOpen(self, cur_handle, timeout=5, poll_frequency=0.5):
        """
        Wait until number of windows increased. Return nothing.
        """
        wait = WebDriverWait(self.driver, timeout, poll_frequency)
        wait.until(EC.new_window_is_opened(cur_handle))
        self.log.debug("The wait :: " + str(timeout) +
                      " :: untill number of winodows increased.")

    def waitUrlChanged(self, current_url, timeout=5, poll_frequency=0.5):
        """
        Wait until curent_url has changed then it returns True, or returns False
        in opposite.
        """
        wait = WebDriverWait(self.driver, timeout, poll_frequency)
        is_changed = wait.until(EC.url_changes(current_url))
        if is_changed:
            self.log.debug("The wait :: " + str(timeout) +
                      " :: until url: " + current_url + " has changed.")
        else:
            self.log.error("The wait :: " + str(timeout) +
                      " :: until url: " + current_url + " HAS NOT changed.")

        return is_changed

    def waitUrlMatchesExpected(self, expected_url, timeout=5, poll_freq=0.5):
        """
        Wait until current url match expected url, then return True, in
        other case return False.
        """
        wait = WebDriverWait(self.driver, timeout, poll_freq)
        is_matches = wait.until(EC.url_matches(expected_url))
        if is_matches:
            self.log.debug("The wait :: " + str(timeout) +
                      " :: until url: " + expected_url + " has matched.")
        else:
            self.log.error("The wait :: " + str(timeout) +
                      " :: until url: " + expected_url + " HAS NOT matched.")
        return is_matches

    def webScroll(self, direction="up"):
        """
        Scroll element on 1000 pixels up or down.
        """
        if direction == "up":
            # Scroll Up
            self.driver.execute_script("window.scrollBy(0, -400);")
            self.log.debug("Web is scrolled up on 400 points.")

        if direction == "down":
            # Scroll Down
            self.driver.execute_script("window.scrollBy(0, 400);")
            self.log.debug("Web is scrolled down on 400 points.")

    def webScrollElement(self, element):
        """
        Scroll to the element.
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.log.debug(
                "Web is scrolled to element: " + str(element) + "." )
        except:
            self.log.error( "Web CAN NOT be scrolled to element: "
                            + str(element) + "." )

    def moveToElementAndClick(self, element, click=False):
        """
        It will place mose over element arg, Click on element if click=True
        return: Noting.

        """
        try:
            action = ActionChains(self.driver)
            if click:
                action.move_to_element(element).click(element).perform()
                self.log.debug("Element: " + str(element) +
                              "in moveToElement hover and clicked.")
            else:
                action.move_to_element(element).perform()
                self.log.debug("Element: " + str(element) +
                              "in moveToElement hover only.")
        except:
            self.log.error("Element: " + str(element) +
                          "in moveToElement NOT hovered and clicked.")

    def findParentWindow(self):
        """
        Return handle object of parent window. If not return None.
        """

        try:
            res = self.driver.current_window_handle
            self.log.debug("Parent Window handle found.")
            return res
        except:
            self.log.error("Parent Window handle was NOT found.")
            return None

    def findAllHandles(self):
        """
        Return handle object of parent window. If not return None.
        """

        try:
            res = self.driver.window_handles
            self.log.debug(("All Window handles found: " + str(res)))
            return res
        except:
            self.log.error("NO Window handles was found.")
            return None

    def switchToWindow(self, handle):
        """
        Switching to the window in handle, Return nothing.
        """
        try:
            self.driver.switch_to_window(handle)
            self.log.debug(("Switched to Window in given handle argument." +
                           str(handle)))
        except:
            self.log.error("CAN NOT Switch to Window in given handle argument.")

    def closeWindow(self):
        """Closing current window. Return nothing."""
        try:
            self.driver.close()
            self.log.debug("Current window had been closed.")
        except:
            self.log.error("Current window CAN NOT been closed.")

    def getElementProperty(self, element, property):
        """
        Return property (string) of element (WebDriver element), return None if
        there in no element, property.
        """
        res = None
        self.log.debug(("Arguments on enter: ", str(element), property))
        try:
            if (element is not None) and (property != ""):
                res = element.get_property(property)
                self.log.debug(("Property: " + str(property) + " of element: " +
                              str(element.text)))
            else:
                self.log.error("Property DOES NOT exists: " + str(property)
                               + " of element: " +
                               str(element.text))
        except:
            self.log.error(("Impossible to get property: " + str(property)
                           + " of element: " + str(element.text)))

        return res





