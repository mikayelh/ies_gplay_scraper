from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import pandas as pd
from worker import go_get_it

# Set the iterations and scrapping speed
iter = 5
wait = 1

# List of URLs to scrape
urls = [
    "https://play.google.com/store/apps/",
    "https://play.google.com/store/apps/details?id=com.facebook.Socal&showAllReviews=true",
    "https://play.google.com/store/apps/details?id=com.facebook.Socal&showAllReviews=true"
]

# Construct executor arguments
args = ((url, iter, wait) for url in urls)

result = []

with PoolExecutor(max_workers=3) as executor:
    for res in executor.map(lambda x: go_get_it(*x), args):
        result.append(res)
