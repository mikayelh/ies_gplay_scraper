import numpy as np
import pandas as pd
import time
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome('chromedriver.exe')
driver.get("https://play.google.com/store/apps/details?id=com.whatsapp&showAllReviews=true")

for i in range(0,200):
        try:
            next_button = driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div')
           """
           <div role="button" class="U26fgb O0WRkf oG5Srb C0oVfc n9lfJ"
           jscontroller="VXdfxd"
           jsaction="click:cOuCgd;
           mousedown:UX7yZ;
           mouseup:lbsD7e;
           mouseenter:tfO1Yc;
           mouseleave:JywGue;
           focus:AHmuwe;
           blur:O22p3e;
           contextmenu:mg9Pef;
           touchstart:p6p2H;
           touchmove:FwuNnf;
           touchend:yfqBxc(preventMouseEvents=true|preventDefault=true);
           touchcancel:JMtRjd;"
           jsshadow=""
           jsname="i3y3Ic"
           aria-disabled="false"
           tabindex="0">
           """
            next_button.click()
        except Exception:
            driver.execute_script("window.scrollTo(0, {to})".format(to = i*1000))
        time.sleep(1)

reviews_div = driver.find_elements_by_xpath('//span[@jsname="bN97Pc"]')
reviews_div[0].text