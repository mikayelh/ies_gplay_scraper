import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import app_reviews as ap

DEBUG = True

options = Options()
if not DEBUG:
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

# EXAMPLE RUN - too short to be usefull
facebook = ap.app_reviews(
    webdriver.Chrome('chromedriver.exe', options = options),
    "https://play.google.com/store/apps/details?id=com.facebook.Socal&showAllReviews=true",
    lang = 'cs'
    )
facebook.run_it(max_iter = 200, rate = 1)
result = facebook.collect_data()