"""
Models page - Testing page with catalog of models after login.
It needs to be launched after login.
"""

import time
from base.basepage import BasePage
import json

class ModelsPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # get dictionary with data testing from data.json
        self.data = json.load(open('utilities/data.json'))

    ########### Service methods #####################
    def getListOfItems(self, locator, locator_type="xpath"):
        """ Return list of elments with 'locator'."""
        return self.getElementList(locator, locator_type)

    def containsTextFlag(self, expected_text, actual_text):
        """Return True, if expectedText in actualTex."""
        if self.util.verifyTextContains(expected_text, actual_text):
            return True
        else:
            return False

    ########### Main Methods #######################
    def verify_num_categories(self, number):
        """Return True, if are 7 items for "Filter by Category"
        on Models Page.TC # 018, in other case False. """

        # Find list of elements categories icons.
        res = self.getListOfItems(self.data["category"])
        if len(res) == number:
            return True
        else:
            return False

    def verifyRows(self, number_of_rows):
        """
        Return True if number found road more/equal 'number_of_rows' arg.
        """
        res = self.getListOfItems(self.data["rows"])
        if len(res) >= number_of_rows:
            return True
        else:
            return False

    def verifyCategoriesUrls(self):
        """
        Return True if after click all categories open right pages.
        "Opened filtered catalog page with:
        1. URL page ""https://stage.fmny.mobi/browse?tag=swim"";
        2. Page contains text ""... models match your search criteria""
        3. There are more than 1 row of models gallery on page;
        """
        # Do not forget lowercase!
        final = (False, [])
        locator = self.data["category"]
        urls = self.getListOfItems(locator)

        # Process every element in list.
        for indx in range(len(urls)):
            # Create list of results
            results = []
            # for protection if element has changed after refresh;
            elem = self.getListOfItems(locator)[indx]
            # Get lowercase of expected text inside of div tag
            expected_text = elem.text.lower()
            elem.click()

            time.sleep(3)  # !!! dicide to exlicite wait.

            ## Handle URL
            # Get actual text on the end of URL after '='
            # 1. URL page need to include title of icon category;
            actual_text = self.getUrl().split('=')[-1]
            results.append(self.containsTextFlag(expected_text, actual_text))

            ## Handle with Text "models match your search criteria"
            # 2. Page contains text ""... models match your search criteria""
            results.append(self.verifyPageIncludesText(self.data["match_text"]))

            ## Handle with number of rows on page.
            # 3. There are more than 1 row of models gallery on page;
            results.append(self.verifyRows(1))
            ## Find final result. No False in list of results.
            self.driver.back()
            if False in results:
                final = (False, results)
                break
            else:
                final = (True, results)

        # Need Back browser after test every time.

        return final # !!!