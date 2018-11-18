"""
Models page - Testing page with catalog of models after login.
It needs to be launched after login.
"""

import utilities.custom_logger as cl
import logging
from base.basepage import BasePage
import time
from base.basepage import BasePage
import json

class ModelsPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # get dictionary with data testing from data.json
        self.data = json.load(open('utilities/data.json'))

    def verify_7_categories(self):
        """Return True, if are 7 items for "Filter by Category"
        on Models Page.TC # 018, in other case False. """
        print("method from Models page")
        # Find list of elements categories icons.
        res = self.getElementList(self.data["category"])
        if len(res) == 7:
            return True
        else:
            return False