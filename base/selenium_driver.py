from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import utilities.custom_logger as cl
from utilities.util import Util
import logging
import time, os

class SeleniumDriver():

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver


    def specialLogLine(self, message):
        """Create Announcement line for the new log."""
        self.log.info(message)

    def screenShot(self, resultMessage):
        """
        Takes screenshots of the current open web page.
        """
        cur_time = str(time.ctime())

        file_name = resultMessage + cur_time + ".png"
        screenshot_dir = "screenshots"
        relative_fname = os.path.join(screenshot_dir, file_name)
        cur_dir = os.getcwd()
        target_dir = os.path.join(cur_dir, relative_fname)

        try:
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)

            self.driver.save_screenshot(target_dir)
            self.log.info("Screenshot: " + str(file_name)
                          + " saved to directory: ../"
                          + str(screenshot_dir))
        except:
            self.log.error('### Exception Occurred with screenshot creation!')
            # print_stack()

    def getUrl(self):
        url = self.driver.current_url
        self.log.info("Current page URL from getUrl method is "+url)
        return url



    def getTitle(self):
        return self.driver.title

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        else:
            self.log.info("Locator type " + locatorType +
                          " not correct/supported")
        return False

    def getElement(self, locator, locatorType="xpath"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info("Element Found in getElement with locator: " + locator +
                          " and  locatorType: " + locatorType)
        except:
            self.log.error("Element NOT found in getElement with locator: " + locator +
                  " and  locatorType: " + locatorType)
        return element

    def getElementList(self, locator, locatorType='xpath'):
        """Get list of elements."""
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_elements(byType, locator)
            self.log.info( "Element List Found with locator: " + locator +
                       " and  locatorType: " + locatorType )
        except:
            self.log.error( "Element LIST not Found with locator: " + locator +
                           " and  locatorType: " + locatorType )
        return element

    def elementClick(self, locator='', locatorType="xpath"):
        """
        Either provide element or a combination of locator and locatorType
        """
        try:
            element = self.getElement(locator, locatorType)
            element.click()
            self.log.info("Clicked on element with locator: " + locator +
                          " locatorType: " + locatorType)
        except:
            self.log.error("Cannot click on the element with locator: " +
                          locator + " locatorType: " + locatorType)
            # print_stack()

    def sendKeys(self, data, locator, locatorType="xpath", element=None):
        """
        Send keys to an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.getElement(locator, locatorType)
                element.clear()
                element.send_keys(data)
                self.log.info( "Sent data '" + data + "' to element with locator: "
                           + locator +
                           " locatorType: " + locatorType )
        except:
            self.log.error( "Cannot send data '" + data + "' to element with locator: "
                           + locator +
                           " locatorType: " + locatorType )
            # print_stack()

    def isElementPresent(self, locator, locatorType="xpath"):
        """ Return True if element Present and False if not. """
        try:
            element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info("Element with locator: " +
                              locator + "Present with locator type: " + locatorType)
                return True
            else:
                self.log.error("Element with locator: " + locator +
                              " NOT Present with locator type: " + locatorType)
                return False
        except:
            self.log.error("Element with locator: " + locator +
                          " NOT Found with locator type: " + locatorType)
            return False

    def getText(self, locator="", locatorType="xpath", element=None, info=""):
        """
        Get 'Text' on an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:  # This means if locator is not empty
                self.log.debug( "In locator condition" )
                element = self.getElement( locator, locatorType )
            self.log.debug( "Before finding text" )
            text = element.text
            self.log.debug("After finding element, size is: " + str(len(text)))
            if len( text ) == 0:
                text = element.get_attribute( "innerText" )
            if len( text ) != 0:
                self.log.info( "Getting text on element :: " + info )
                self.log.info( "The text is :: '" + text + "'" )
                text = text.strip()
        except:
            self.log.error( "Failed to get text on element " + info )
            # print_stack()
            text = None
        return text

    def isElementPresece(self, locator="", locatorType="xpath", element=None):
        """
        Check if element is present ->
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info("Element present with locator: " + locator +
                              " locatorType: " + locatorType)
                return True
            else:
                self.log.info("Element not present with locator: " + locator +
                              " locatorType: " + locatorType)
                return False
        except:
            print("Element not found")
            return False

    def isElementDisplayed(self, locator="", locatorType="xpath", element=None):
        """
        Check if element is displayed
        Either provide element or a combination of locator and locatorType
        """
        isDisplayed = False
        try:
            if locator:  # This means if locator is not empty
                element = self.getElement( locator, locatorType )
            if element is not None:
                isDisplayed = element.is_displayed()
                self.log.info( "Element is displayed with locator: " + locator +
                               " locatorType: " + locatorType )
                return True
            else:
                self.log.error( "Element not displayed with locator: " + locator +
                               " locatorType: " + locatorType )
                return False
        except:
            print( "Element not found" )
            return False

    def waitForClickElement(self, locator, click=False, locatorType="xpath",
                               timeout=5, pollFrequency=0.5):
        """Wait Element with locator, and click after found if True. """
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                  " :: seconds for element '" + locator + "' to be clickable")
            wait = WebDriverWait(self.driver, timeout, pollFrequency
                                 )
            element = wait.until(EC.element_to_be_clickable((byType, locator)))
            self.log.info("Element '" + locator + "' appeared " + locator + " on the web page")
            if click:
                element.click()
                self.log.info("Element '" + locator + "' clicked with locator " + locator + " on the web page")
        except:
            self.log.error("Element '" + locator + "' NOT appeared " + locator + " on the web page")
            # print_stack()
        return element

    def waitElementLocated(self, locator, locatorType="xpath",
                               timeout=5, pollFrequency=0.5):
        """Wait until Element will be located with locator. Return element. """
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                  " :: seconds for element to be LOCATED")
            wait = WebDriverWait(self.driver, timeout, pollFrequency)
            element = wait.until(EC.presence_of_element_located((byType, locator)))
            self.log.info("Confirmed presence of element located with locator: " + locator + " on the web page")
        except:
            self.log.error("NOT Confirmed presence of element with locator: " + locator + " on the web page")
            # print_stack()
        return element

    def webScroll(self, direction="up"):
        """
        Scroll element on 1000 pixels up or down.
        """
        if direction == "up":
            # Scroll Up
            self.driver.execute_script( "window.scrollBy(0, -1000);" )

        if direction == "down":
            # Scroll Down
            self.driver.execute_script( "window.scrollBy(0, 1000);" )

    def webScrollElement(self, element):
        """
        Scroll element on 1000 pixels up or down.
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.log.info( "Web is scrolled to element: " + element.text + "." )
        except:
            self.log.error( "Web CAN NOT be scrolled to element: " + element.text + "." )