"""
Models page - Testing page with catalog of models after login.
It needs to be launched after login.
"""

import time

from base.main_driver import MainDriver
import random

class ModelsPage(MainDriver):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    ########### Service methods #####################
    def openModelPage(self):
        # open page with URL "models_url": "https://stage1.fmny.mobi/browse"
        self.openUrlPage(self.data["models_url"])



    def getListOfItems(self, locator, locator_type="xpath"):
        """ Return list of elmenets with 'locator'."""
        return self.getElementList(locator, locator_type)

    def containsTextFlag(self, expected_text, actual_text):
        """Return True, if expectedText in actualTex."""
        if self.util.actualTextContainsExpected(expected_text, actual_text):
            return True
        else:
            return False

    def scrolELementForClick(self, element):
        # scroll that element will be seen.
        self.webScrollElement(element)
        # scroll up to move element from top menu panel
        self.webScroll("up")

    def collectListModelsNames(self, locator, locator_type="xpath"):
        """
        Return the list of the names of models in elments of rows in
        models' gallery. locator to the "Name of model" in the rows of models.
        """
        return self.getElementList(locator, locator_type)


    def portfolioControl(self, elements_num, elements_locator, names_locator,
                        expected_el_locator):
        """
        Universal method for control of portfolio opening in new
        window (the same for avatar and for button "See Portfolio"
        For this method arguments needed:
        Return true if all elements opened, found and equal.
        """

        # number will be randomly tested
        testing_num = elements_num

        # list of names for comparing with name in Portfolio
        names = self.waitAllElementsLocated(names_locator)

        size_of_index = len(names)
        random_index_list = self.util.randomIndexList(
            size_of_index, testing_num)

        result = []
        for indx in random_index_list:
            # collect all "See Portfolio" web elements
            elements_list = self.getElementList(elements_locator)

            # collect all names of current models of gallery rows.
            names = self.collectListModelsNames(names_locator)

            # For current randomly chosen name
            expected_name = self.getText(names[indx])

            # Find parent handle -> Main Window
            parent_window = self.findParentWindow()

            # Scroll to the element seen for clicking
            self.scrolELementForClick(elements_list[indx])
            # Click by JS, to open new window with profile
            new_element = self.waitAllElementsLocated(elements_locator)
            self.moveToElementAndClick(new_element[indx], True)

            # wait until EC.new_window_is_opened(current_handles)
            self.waitNewWindowOpen([parent_window], 10)
            # Find all handles
            handles = self.findAllHandles()
            # Change the window
            current_res = False
            for handle in handles:
                if handle != parent_window:
                    self.switchToWindow(handle)
                    # Find text element with Name.
                    actual_el = self.waitElementLocated(expected_el_locator)
                    actual_name = self.getText(actual_el)

                    # Check that found text contains expectedText
                    current_res = self.util.actualTextContainsExpected(
                        expected_name, actual_name)
                    self.closeWindow()
                    # Switch back to parent window.
                    self.switchToWindow(parent_window)
                    current_res = True
            # Actual name doesn't consists expected name.
            result.append(current_res)

            # Add result in result with tuple (Boolean, "model's name")
            # result = (expected_name == actual_name)

        return self.util.absentFalseInList(result)

    def newFrameControl(self, elements_num, elements_locator, locator_rows,
                        expected_element_locator,
                        expected_element_close, element_locator_type="xpath",
                        expected_el_close_type="xpath", image_per_row=4):
        """
        It takes some argument with locators and return the True if the
        element with expected_locator found on opened frame.
        Return False if any of the numbers try will not True.
        """

        rows = self.waitAllElementsLocated(locator_rows, "xpath", 10)

        random_index_list = self.util.randomIndexList(
            len(rows), elements_num)
        # Take only first minimal number of rows for testing (5)
        # in the second section there are 4 divs with "photo container"
        # We need to check 20 (5 * 4) photo container elements is clickable

        result = []
        for indx in random_index_list:
            # Every models has 4 images in row so we need check 0...3 images
            # for every random_index_list: (0 + indx ) to (3 + indx ) element
            rows = self.waitAllElementsLocated(locator_rows)
            current_element = rows[indx]
            self.scrolELementForClick(current_element)

            for counter in range(image_per_row):
                cur_index = indx * image_per_row + counter

                images_elements = self.waitAllElementsLocated(
                    elements_locator, element_locator_type)
                self.elementClick("", "", images_elements[cur_index])

                # Wait control element is available;
                control_el = self.waitElementLocated(expected_element_locator)
                result.append(self.isElementDisplayed("", "", control_el))
                # Closing new window with closing element
                self.waitForClickElement(expected_element_close,
                                   True, expected_el_close_type)

        return  self.util.absentFalseInList(result)

    ########### Main Methods #######################
    def actualCategoriesNumEqualExpected(self):
        """Return True, if are 7 items for "Filter by Category"
        on Models Page.TC # 018, in other case False. """

        # Find list of elements categories icons.
        actual_num = len(self.waitAllElementsLocated(
                                        self.data["category"], "xpath", 10))

        # !!! move to the Util() class with logs and try:
        expected_num = self.data["number_of_categories"]

        return self.util.actualNumbersMatchExpected(expected_num, actual_num)

    def verifyRows(self, num=None):
        """
        Return True if number of found rows more/equal 'number_rows' arg.
        """
        if num is None:
            min_num = self.data["minimal_number_rows"]
        else:
            min_num = num
        return len(self.getListOfItems(self.data["rows"])) >= min_num


    def verifyCategoriesUrls(self):
        """
        Return True if after click all categories open right pages.
        "Opened filtered catalog page with:
        1. URL page ""https://stage.fmny.mobi/browse?tag=swim"";
        2. Page contains text ""... models match your search criteria""
        3. There are more than 1 row of models gallery on page;
        """
        urls = self.getListOfItems(self.data["category"])
        results = [False]
        # Process every element in list.
        for indx in range(1):    #   len(urls)): # !!! change for production
            # for protection if element has changed after refresh;
            element = urls[indx]
            # Get lowercase of expected text inside of div tag
            expected_text = element.text.lower()
            cur_url = self.getUrl()
            self.elementClick("", "", element)

            self.waitUrlChanged(cur_url)
            ## Handle URL
            # Get actual text on the end of URL after '='
            # 1. URL page need to include title of icon category;
            actual_text = self.getUrl().split('=')[-1]
            is_equal = self.util.verifyTextMatch(
                                             expected_text, actual_text
                                                 )
            results = [is_equal]

            ## Handle with Text "modelsu match your search criteria"
            # 2. Page contains text "models match"
            models_match = self.waitElementVisible(self.data["models_match"])
            results.append(models_match is not None)

            ## Handle with number of rows on page.
            # 3. There are more than "minimal_num_rows" of models gallery;
            results.append(self.verifyRows())
            ## Find final result. No False in list of results.
            self.pushBrowserBackBtn()

        # Need Back browser after test every time.

        return (self.util.absentFalseInList(results))

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
        result = self.portfolioControl(
            self.data["number_avatars"],
            self.data["avatars"],
            self.data["names"],
            self.data["name_in_profile"]
        )

        return result

    def verifyNumberImagesRow(self):
        """
        Return: True if all first "minimal number of rows" in gallery of Models
        have "images_per_row" (4) images per row.
        """
        result = self.newFrameControl(
            self.data["number_images_checking"],
            "photo-container",
            self.data["rows"],
            self.data["name_in_gallery"],
            self.data["image_library_close"],
            "class"  # Need to be last to avoid using "xpath"
        )

        return result

    def verifyBookModelButton(self):
        """
        Return True if possible click and get booking page for the
        randomly chosen 3 (booking_nu) Models in rows of Model page.
        """

        result = self.newFrameControl(
            self.data["booking_num"],
            self.data["book_locator"],
            self.data["rows"],
            self.data["booking_page_text"],
            self.data["almost_there_close"],
            "xpath",
            "xpath",
            1
        )


        return result

    def verifyFavoriteButtons(self):
        """
        Return True if all models in gallery with number
        self.data["favorite_num"] open "Add to Favorites" page.
        If not: False
        """

        result = self.newFrameControl(
            self.data["favorite_num"],
            self.data["favorite_btn"],
            self.data["rows"],
            self.data["favorite_elem"],
            self.data["close_favorite"],
            "xpath",
            "xpath",
            1
        )

        return result

    def verifySeePortfolioButton(self):
        """
        Return True if all randomly chosen models in gallery with number
        self.data["favorite_num"] open "Portfolio" window.
        Portfolio page include the name the same as the model's row in gallery.
        If not: False
        """

        # Create universal method for control of portfolio opening in new
        # window (the same for avatar and for button "See Portfolio"
        # For this method arguments needed:
        # Xpath for the names on gallery rows. : data.json:"names"
        # Xpath for the buttons "See Portfolio" : data.json:"see_portfolio"
        # Number of models will be tested: data.json:"portfolio_num"

        result = self.portfolioControl(
            self.data["portfolio_num"],
            self.data["see_portfolio"],
            self.data["names"],
            self.data["name_in_profile"]
        )
        return result
