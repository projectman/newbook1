"""
Models page - Testing page with list of models and some model after login.
It needs to be launched after login or
"if not logged in: login" add method in Selenium_Driver class?
"""

import time
from base.selenium_driver import SeleniumDriver
import utilities.custom_logger as cl
import logging
from base.basepage import BasePage

class Models