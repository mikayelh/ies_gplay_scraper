import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import app_reviews as ap

DEBUG = True

options = Options()
if not DEBUG:
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

# running the scrapper for one google application
next_app = ap.app_reviews(
    webdriver.Chrome('chromedriver.exe', options = options),
    "https://play.google.com/store/apps/details?id=com.facebook.Socal&showAllReviews=true",
    lang = 'en'
    )
next_app.run_it(max_iter = 5, rate = 1)
result = next_app.collect_data()