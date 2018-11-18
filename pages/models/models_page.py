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

class Models(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # get dictionary with data testing from data.json
        self.data = json.load(open('utilities/data.json'))