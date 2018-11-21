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
        """ Return list of elmenets with 'locator'."""
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
        actual_num = len(self.getListOfItems(self.data["category"]))

        # !!! move to the Util() class with logs and try:
        expected_num = self.data["number_of_categories"]

        return self.util.verifyNumbersMatch(expected_num, actual_num)

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
        for indx in range(1):    #   len(urls)): # !!! change for production
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
            results.append(self.util.verifyTextContains(
                                                    expected_text, actual_text))

            ## Handle with Text "modelsu match your search criteria"
            # 2. Page contains text ""... models match your search criteria""
            results.append(self.verifyPageIncludesText(self.data["match_text"]))

            ## Handle with number of rows on page.
            # 3. There are more than 1 row of models gallery on page;
            results.append(self.verifyRows(1))
            ## Find final result. No False in list of results.
            self.driver.back()  #  !!! change to the cross.click() on icon catergory
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
        Return Tuple of [0] boolean results compares of names
        with tuple of names for comparing (True, (Name_expected, Name_actual).
         if after clicking 'number' eventually chosen avatars,
        will check that it alive profile linked to avatar.
        number of avatars for checking described by data.json:"number_avatars";
        """
        # collect all avatars of gallery rows.
        avatars = self.getElementList(self.data["avatars"])
        # collect all names of current models of gallery rows.
        names = self.getElementList(self.data["names"])

        # Chose random avatar from list with index... ;
        index_list = list(range(len(avatars)))
        res_random_avatars = []
        res_random_names = []
        # Arrange loop for the number of circles as in "number_avatars" json.
        for _ in range(self.data["number_avatars"]):
            # get random item from basic list of indexes
            random_indx = random.choice(index_list)

            # find the current index of random item in basic list of indexes
            index = index_list.index(random_indx)

            # took the index element from the total list
            random_element_index = index_list.pop(index)

            # took from the avatars hrefs afttribute of elem the item with index
            href_property = self.getElementProperty(
                avatars[random_element_index], "href")

            # include in list of href locator only after 25 element
            res_random_avatars.append(href_property[24:])
            res_random_names.append(names[random_element_index])

        # Processing of list randomly chosen names and avatars.
        # Took the name with this index
        result =[]
        for _ in range(len(res_random_names)):
            # For current randomly chosen name
            expected_name = self.getText(res_random_names[_])

            # Find parent handle -> Main Window
            parent_window = self.findParentWindow()

            # click on the avatar
            href = res_random_avatars[_]
            locator = "//a[@href='" + href + "']"
            avatar = self.waitElementLocated(locator)
            # scroll that element will be seen.
            self.webScrollElement(avatar)
            # scroll from top menu panel
            self.webScroll("up")
            # Click by JS, to open new window with profile
            self.moveToElementAndClick(avatar, True)

            # !!! Refactor via waiting that list of handles > 1
            time.sleep(5)
            # Find all handles
            handles = self.findAllHandles()
            # Change the window
            current_res = False
            actual_name = ""
            for handle in handles:
                if handle not in parent_window:
                    self.switchToWindow(handle)
                    # Find text element with Name.
                    actual_el = self.waitElementLocated(
                        self.data["name_in_profile"])
                    actual_name = self.getText(actual_el)

                    # Check that found text contains expectedText
                    current_res = self.util.verifyTextContains(
                                            expected_name, actual_name)
                    self.closeWindow()
                    # Switch back to parent window.
                    self.switchToWindow(parent_window)
                else:
                    actual_name = "Name was not found."

            # Actual name doesn't consists expected name.
            result.append((current_res, (expected_name, actual_name)))

            # Add result in result with tuple (Boolean, "model's name")
            # result = (expected_name == actual_name)

        return result

    def verifyNumberImagesRow(self):
        """
        Return: True if all first "minimal number of rows" in gallery of Models
        have "images_per_row" (4) images per row.
        """
        # Collect Rows
        rows = self.getElementList(self.data["rows"])
        # Take only first minimal number of rows for testing (5)
        used = self.data["minimal_number_rows"]
        # in the second section there are 4 divs with "photo container"
        # We need to check 20 (5 * 4) photo container elements is clickable
        images_el = self.getElementList("photo-container", "class")

        print("images len:", len(images_el))
        res = False
        for _ in range(used * 4):
            # Collect number of images in row
            # Get href of row to recognise current row
            is_clicable = self.isElementClickable(images_el[_])

            # Collect all images for the curren row.
            # Create xpath for the images inherited curren row with href
            # Every row: <nb-model-listt-item> has 2 sections.


            # Compare number of images in the row with "images per row"

            # Create res_list result list of tuples with Bulean then Tuples
            # of numbers expected and actual.