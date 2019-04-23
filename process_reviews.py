import pandas as pd
from selenium import webdriver

import app_reviews as apr

# EXAMPLE RUN - too short to be usefull
whatsap = apr.app_reviews(
    webdriver.Chrome('chromedriver.exe'),
    "https://play.google.com/store/apps/details?id=com.whatsapp&showAllReviews=true"
    )
whatsap.run_it(max_iter = 20, rate = 0.8)
whatsap.unwrap_reviews()
result = whatsap.collect_data()