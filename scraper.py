import numpy as np
import pandas as pd
import time
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException, WebDriverException
from bs4 import BeautifulSoup
import re

class app_reviews:
    """
    Class definition of the webdriver used for reviews scrapping.
    """
    def __init__(self, driver, url):
        self.url = url
        self.position = 0
        self.driver = driver
        self.driver.get(url)
    #
    def move_to(self, pos):
        """
        Move to a position defined by Y axis pixels.
        """
        self.driver.execute_script("window.scrollTo(0, {to})".format(to = pos))
    #
    def move_it(self, pos = -1, offset = 10000):
        """
        Scroll further down, loading more reviews (via button click) if possible.
        """
        try:
            next_button = self.driver.find_element_by_xpath('//div[@jsname="i3y3Ic"]')
            next_button.click()
        except (NoSuchElementException, WebDriverException):
            if pos == -1:
                pos = self.position
            self.move_to(pos + offset)
        self.position = self.driver.execute_script("return window.pageYOffset;")
    #
    def unwrap_reviews(self):
        """
        Unwrap all shortened reviews.
        """
        self.move_to(0)
        unwrapped = self.driver.find_elements_by_xpath('//button[@jsname="gxjVle"]')
        for click in unwrapped:
            try:
                click.click()
            except (ElementNotVisibleException, WebDriverException):
                pass
    #
    def run_it(self, max_iter = 1000, rate = 1):
        """
        Start the process of loading the reviews.
        """
        i = 0
        while i < max_iter:
            self.move_it()
            i += 1
            time.sleep(rate)
        self.unwrap_reviews()
    #
    def extract_short(self):
        """
        Extract the short reviews.
        """
        reviews_div = self.driver.find_elements_by_xpath('//span[@jsname="bN97Pc"]')
        reviews_txt = [i.text for i in reviews_div]
        return(reviews_txt)
    #
    def extract_long(self):
        """
        Extract the long (wrapped) reviews.
        """
        unwrapped_div = self.driver.find_elements_by_xpath('//span[@jsname="fbQN7e"]')
        unwrapped_txt = [i.text for i in unwrapped_div]
        return(unwrapped_txt)
    #
    def collect_reviews(self):
        """
        Collect all reviews.
        """
        short = self.extract_short()
        long = self.extract_long()
        empty_fit = [l == '' for l in long] != [s == '' for s in short]
        if empty_fit:
            reviews = [val + long[ix] for ix, val in enumerate(short)]
        else:
            reviews = [short, long]
        return(reviews)
    #
    def collect_rating(self):
        """
        Colect user ratings of the app.
        """
        rating = self.driver.find_elements_by_xpath(
            '//span[@class="nt2C1d"]/div[@class="pf5lIe"]/div[contains(@aria-label,"Hodnocení")]'
            )
        rat_int = [
            re.findall('\d+', r.get_attribute('aria-label'))[0]
                for r in rating
        ]
        return(rat_int)
    #
    def collect_support(self):
        """
        Collect the support of the review.
        """
        support = self.driver.find_elements_by_xpath(
            '//div[@class = "jUL89d y92BAb"]'
            )
        return([s.text for s in support])
    #
    def collect_data(self):
        """
        Collect all data into a pandas.DataFrame
        """
        return(
            pd.DataFrame({
                'review'  : self.collect_reviews(),
                'rating'  : self.collect_rating(),
                'support' : self.collect_support()
            })
        )

# EXAMPLE RUN - too short to be usefull
whatsap = app_reviews(
    webdriver.Chrome('chromedriver.exe'),
    "https://play.google.com/store/apps/details?id=com.whatsapp&showAllReviews=true"
    )
whatsap.run_it(max_iter = 10, rate = 0.8)
result = whatsap.collect_data()