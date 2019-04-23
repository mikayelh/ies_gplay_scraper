import numpy as np
import pandas as pd
import time
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException, WebDriverException
from bs4 import BeautifulSoup
import re

class app_reviews:
    """
    Class definition of the webdriver used for reviews scrapping

    Parameters
    ----------
    driver : selenium.webdriver.<driver>.webdriver.WebDriver
        a webdriver to be used
    second : str
        URL of the app

    Attributes
    ----------
    url : str
        URL of the app
    position : int
        latest position achieved using `move_it` method
    driver : selenium.webdriver.<driver>.webdriver.WebDriver
        exposing the webdriver used for scrapping
    """
    def __init__(self, driver, url):
        """
        Starting own webdriver, initialize the scrapping of a new application
        """
        self.url = url
        self.position = 0
        self.driver = driver
        self.driver.get(url)
    #
    def move_to(self, pos):
        """
        Move driver to a position defined by Y axis pixels

        Parameters
        ----------
        pos : int
            a pixel representation of the target position (scroll to)
        """
        self.driver.execute_script("window.scrollTo(0, {to})".format(to = pos))
    #
    def move_it(self, pos = -1, offset = 10000):
        """
        Scroll further down, loading more reviews (via button click) if possible

        Parameters
        ----------
        pos : int
            a pixel representation of the original position (scroll from)
        offset : int
            a number of pixels to be scrolled down
            - should be large enough to hit the end of page
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
        Unwrap all shortened reviews
        Walks through the loaded reviews and clicks every 'Show full review' button
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
        Start the process of loading the reviews

        Parameters
        ----------
        max_iter : int
            a number defining how many times will be method `move_it` used
        rate : int
            waiting time between subsequent calls to method `move_it`
            - should be large enough for the webdriver to load new content
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
        Extract the short reviews

        Returns
        -------
        list
            list containing short reviews
            - position is empty ('') for unwrapped reviews
        """
        reviews_div = self.driver.find_elements_by_xpath('//span[@jsname="bN97Pc"]')
        reviews_txt = [i.text for i in reviews_div]
        return(reviews_txt)
    #
    def extract_long(self):
        """
        Extract the long (wrapped) reviews

        Returns
        -------
        list
            list containing long reviews
            - position is empty ('') for short reviews
        """
        unwrapped_div = self.driver.find_elements_by_xpath('//span[@jsname="fbQN7e"]')
        unwrapped_txt = [i.text for i in unwrapped_div]
        return(unwrapped_txt)
    #
    def collect_reviews(self):
        """
        Collect all reviews. Tries to match short and long reviews into a pandas.DataFrame

        Returns
        -------
        pandas.core.frame.DataFrame
            if reviews were matched perfectly
        list
            otherwise
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
        Colect user ratings of the app

        Returns
        -------
        list
            list containing how was the app rated by user
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
        Collect the support of the review

        Returns
        -------
        list
            list containing how was the review rated by other users
        """
        support = self.driver.find_elements_by_xpath(
            '//div[@class = "jUL89d y92BAb"]'
            )
        return([s.text for s in support])
    #
    def collect_data(self):
        """
        Collect all data into a pandas.DataFrame

        Returns
        -------
        pandas.core.frame.DataFrame
            table of reviews, ratings and support
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