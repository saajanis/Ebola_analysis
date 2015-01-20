
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import sys
import os
 
import unittest, time, re
 
class Sel(unittest.TestCase):
    def setUp(self):
        chromedriver = "/Users/Saajan/Documents/workspace/Dependencies/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)
        #self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://twitter.com"
        self.verificationErrors = []
        self.accept_next_alert = True
    def test_sel(self):
        driver = self.driver
        delay = 3
        driver.get(self.base_url + "/search?q=guinea ebola AND (flu OR fever OR headache OR pain OR weakness OR fatigue OR cough OR stomach OR pain OR vomiting OR diarrhea OR vomit OR hemorrhage OR haemorhagic OR bleeding OR bruising OR suspected OR cases OR outbreak OR death OR spread OR )  lang%3Aen since%3A2014-03-24 until%3A2014-03-27&src=typd")
        driver.find_element_by_link_text("All").click()
        for i in range(1,1000000):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
        html_source = driver.page_source
        data = html_source.encode('utf-8')
 
 
if __name__ == "__main__":
    unittest.main()