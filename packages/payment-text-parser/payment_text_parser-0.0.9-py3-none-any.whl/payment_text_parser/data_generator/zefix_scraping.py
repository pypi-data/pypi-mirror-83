"""
 * (C) Copyright 2020 Alpina Analytics GmbH
 *
 * This file is part of payment_text_parser
 *
 * payment_text_parser is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * payment_text_parser is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with payment_text_parser.  If not, see <http://www.gnu.org/licenses/>.
"""

import urllib
import urllib.request
from bs4 import BeautifulSoup
import string
import time
import pickle
import os

SAVE_FILE = True
DST_DIR = '../data/scraped_data'

from selenium import webdriver

def get_companies_per_page(letters='aa'):
    url = 'https://www.zefix.ch/fr/search/entity/list?name={}&searchType=undefined'.format(letters)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    #TODO Add driver to path and test
    browser = webdriver.Chrome("/Users/Pierre/Code/perso/swiftScraper/chromedriver",options=options)
    browser.get(url) #navigate to the page
    browser.implicitly_wait(10)
    res = []
    res_prev_ = []
    
    while True:
        
        res_ = []
        table = browser.find_elements_by_xpath("//td[contains(@class, 'ng-scope')]//div[contains(@class,'company-name')]")
        #table = browser.find_elements_by_xpath("//div[contains(@ng-swipe-right, 'app')]//*[@class='zefix-search-results']//*/a[@class='ng-binding']")
                
        for t in table:
            res_.append(t.text)
        
        res.extend(res_)

        if len(table) == 0 or res_ == res_prev_ :
            browser.close()
            break
        
        # Next page
        res_prev_ = res_
        el = browser.find_elements_by_xpath("//span[contains(@class, 'icon icon--right')]")
        el[0].click()
        
    return res


ls = []
for l1 in string.ascii_lowercase:
#for l1 in ['a']:
    for l2 in string.ascii_lowercase:
    #for l2 in ['a']:
        ll = l1+l2
        try:
            ls.extend(get_companies_per_page(ll))
        except:
            pass
 
    # Saving

        file = os.path.join(DST_DIR,'ORG2.pickle')
        res = {'individuals': ls}
        if SAVE_FILE:
            with open(file, 'wb') as f:
                pickle.dump(res, f, protocol=pickle.HIGHEST_PROTOCOL)

        print("Data saved - Intermediate saving")

print("Data saved, process terminated.")
