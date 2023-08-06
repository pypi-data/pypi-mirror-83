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

SAVE_FILE = False
DST_DIR = './data/scraped_data'

# Class

class Registery(object):
    
    def __init__(self):
        
        self.individuals = []
        self.addresses = []
      
    @staticmethod
    def get_soup(url):
        f = urllib.request.urlopen(url)
        page = f.read()
        soup = BeautifulSoup(page,"lxml")
        return soup
          
    def get_individuals(self,url):
        
        soup = Registery.get_soup(url)
        myspans = soup.findAll("span", {"class": "listing-title"})
        for e in myspans:
            e_clean = e.text.replace('\n','')
            self.individuals.append(e_clean)
        
        return self
    
    def get_addresses(self,url):
        
        soup = Registery.get_soup(url)
        mydivs = soup.findAll("div", {"class": "listing-address small"})
        for e in mydivs:
            e_clean = e.text.replace('\n','')
            self.addresses.append(e_clean)
        
        return self

# Functions

def get_data(entity):
    
    URL = 'https://tel.local.ch/fr/q/{cc}*.html?page={p}&typeref={e}'
    N_PAGE = 100      
    r = Registery()
    
    alphabet = string.ascii_lowercase
    
    # Search
    
    for c1 in alphabet:
        
        start_time = time.time()
        
        for c2 in alphabet:
            cc = c1+c2
            print("Letter combination :",cc)
            for p in range(1,N_PAGE): 
                print("Page :",p)
                url = URL.format(cc=cc,p=p,e=entity)
                try:
                    r.get_individuals(url)
                    r.get_addresses(url)
                except:
                    pass
                
        elapsed_time = time.time() - start_time
        print("Time elapsed for letter {} :".format(c1),elapsed_time,"s")

    # Saving
        
    entity_normalized = {'res' : 'PER', 'bus':'ORG'}
    file = os.path.join(DST_DIR,'{}.pickle'.format(entity_normalized[entity]))
    res = {'individuals': r.individuals, 'addresses' : r.addresses}
    if SAVE_FILE:
        with open(file, 'wb') as f:
            pickle.dump(res, f, protocol=pickle.HIGHEST_PROTOCOL)
        
    print("Data saved.")

# Main (ca. 12h for each entity type => 24h search)

def main():  
    for entity in ['res','bus']:
        get_data(entity)

if __name__ == "__main__":
    main()