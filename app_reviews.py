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
    url : str
        URL of the app
    lang : str
        driver locale, expected to be either 'cs' or 'en'

    Attributes
    ----------
    url : str
        URL of the app
    position : int
        latest position achieved using `move_it` method
    driver : selenium.webdriver.<driver>.webdriver.WebDriver
        exposing the webdriver used for scrapping
    source : bs4.BeautifulSoup
        exposing the BeautifulSoup parsed webpage source
    """
    def __init__(self, driver, url, lang = 'en'):
        """
        Starting own webdriver, initialize the scrapping of a new application
        """
        self.url = url
        self.position = 0
        self.driver = driver
        self.driver.get(url)
        self.source = -1
        if lang in ['en', 'cs']:
            self.lang = lang
        else:
            raise ValueError("The lang is expected to be either 'cs' or 'en'")
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
        Scroll further down, loading more reviews (via button click) if possible.
        Can be used for incremental scrolling.

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
    def get_source(self):
        """
        Parse and save the webpage source
        """
        self.source = -1
        self.source = BeautifulSoup(self.driver.page_source, features = "lxml")
        return
    #
    def val_source(self):
        """
        Validate the page was parsed and saved.
        """
        if self.source == -1:
            raise ValueError('The page was not parsed. Make sure you run `get_source()` method first.')
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
        self.get_source()
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
        self.val_source()
        reviews_div = self.source.select('span[jsname="bN97Pc"]')
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
        self.val_source()
        unwrapped_div = self.source.select('span[jsname="fbQN7e"]')
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
        self.val_source()
        if self.lang == 'cs':
            rating = self.source.select('span.nt2C1d > div.pf5lIe > div[aria-label*=Hodnocení]')
        else:
            rating = self.source.select('span.nt2C1d > div.pf5lIe > div[aria-label*=Rated]')
        rat_int = [
            re.findall('\d+', r.get('aria-label'))[0]
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
        self.val_source()
        support = self.source.select('div[class="jUL89d y92BAb"]')
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