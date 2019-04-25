import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import app_reviews as ap

DEBUG = True

if not DEBUG:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
else:
    options = Options()

# EXAMPLE RUN - too short to be usefull
whatsap = ap.app_reviews(
    webdriver.Chrome('chromedriver.exe', options = options),
    "https://play.google.com/store/apps/details?id=com.facebook.Socal&showAllReviews=true"
    )
whatsap.run_it(max_iter = 10, rate = 0.7)
result = whatsap.collect_data()