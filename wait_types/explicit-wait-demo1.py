from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

class ExplicitWaitDemo1():

    def test(self):
        baseUrl = "http://www.expedia.com"
        driver = webdriver.Firefox()
        driver.implicitly_wait(.5)
        driver.maximize_window()
        driver.get(baseUrl)
        driver.find_element(By.ID, "tab-flight-tab-hp").click()
        driver.find_element(By.ID, "flight-origin-hp-flight").send_keys("SFO")
        driver.find_element(By.ID, "flight-destination-hp-flight").send_keys("NYC")
        driver.find_element(By.ID, "flight-departing-hp-flight").send_keys("09/24/2018")
        returnDate = driver.find_element(By.ID, "flight-returning-hp-flight")
        returnDate.clear()
        returnDate.send_keys("10/15/2018")
        driver.find_element(By.CSS_SELECTOR,
                            "#gcw-flights-form-hp-flight [type='submit']").click()

        wait = WebDriverWait(driver, 10)

        element = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                         "/html//section[@id='columnAFilter']/div[@id='filter-container']/fieldset[@id='stops']/div/label[1]/div/div[1]/input[@name='fs0']")))
        # element = wait.until(EC.element_to_be_clickable((By.ID, "stopFilter_stops-0")))
        # element = driver.find_element(By.XPATH,
        element.click()

        time.sleep(5)
        driver.quit()

ff = ExplicitWaitDemo1()
ff.test()