from typing import List
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import app_reviews as ap

def go_get_it(url:str, iter:int, wait:float) -> List[pd.DataFrame]:
    """
    Handle the scrapping of reviews in the specified URL.
    Internally initializes an instance of `app_reviews` class,
    and calls following methods
        - run_it(max_iter = iter, rate = wait)
        - collect_data()

    Parameters
    ----------
    url : str
        URL of the application reviews
    iter : int
        how many iterations of movement to run
    wait : fload
        waiting time before iterations (for the page to load)
    
    Returns
    -------
    pd.DataFrame
        a table of scrapped data, as returned by `app_reviews.collect_data()`
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    app = ap.app_reviews(
        webdriver.Chrome('chromedriver.exe', options = options),
        url, lang = 'en'
        )
    # don't kill everything for one broken page
    try:
        app.run_it(max_iter = iter, rate = wait)
        collected = app.collect_data()
        app.driver.close()
    except Exception as err:
        # make sure driver gets always closed
        app.driver.close()
        collected = err
    return(collected)