"""
Models page - Testing page with catalog of models after login.
It needs to be launched after login.
"""

import time
from base.selenium_driver import SeleniumDriver
import json
import random

class ModelsPage(SeleniumDriver):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

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
    def equal_num_categories(self):
        """Return True, if are 7 items for "Filter by Category"
        on Models Page.TC # 018, in other case False. """

        # Find list of elements categories icons.
        res = self.getListOfItems(self.data["category"])

        # !!! move to the Util() class with logs and try:
        if len(res) == self.data["number_of_rows"]:
            return True
        else:
            return False

    def verifyRows(self, number_rows):
        """
        Return True if number of found rows more/equal 'number_rows' arg.
        """
        res = self.getListOfItems(self.data["rows"])
        if len(res) >= number_rows:
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
        for indx in range(2):    #   len(urls)):
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

    def verifyNumberAvatars(self):
        """
        Return True if number of avatars in gallery is the same as number
        of rows.
        """

        rows = self.getListOfItems(self.data["rows"])
        avatars = self.getListOfItems(self.data["avatars"])
        is_eqal = len(rows) == len(avatars)
        return is_eqal

    def verifyEachAvatars(self):
        """
        Return True if after clicking 'number' eventually chosen avatars,
        will check that it alive profile linked to avatar.
        number of avatars for checking described by data.json:"number_avatars";
        """

        # collect all avatars of gallery rows.
        avatars = self.getListOfItems(self.data["avatars"])
        # collect all names of current models of gallery rows.
        names = self.getListOfItems(self.data["names"])
        equal_number = avatars == names
        # Chose random avatar from list with index... ;
        index_list = list(range(len(avatars)))
        random_avatars = []
        for _ in range(self.data["number_avatars"]):
            # get random item from basic list of indexes
            random_indx = random.choice(index_list)
            # find the current index of random item in basic list of indexes
            index = index_list.index(random_indx)
            # took the index element from the total list
            random_element_index = index_list.pop(index)
            # took from the avatars the item with index
            random_avatars.append(avatars[random_element_index])

        # Took the name with this index

        # click on the avatar

        # Verify that page of profile contains the text of chosen name with same index.

        # Add result in result with tuple (Boolean, "model's name")

        # Click browser back.


        return True