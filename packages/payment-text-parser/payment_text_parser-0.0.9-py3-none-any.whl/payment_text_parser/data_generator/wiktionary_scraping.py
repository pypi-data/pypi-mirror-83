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
import xml.etree.ElementTree as ET
import pickle
import os

DST_DIR = './data/scraped_data'

# Lexicons

def get_soup(url):
        f = urllib.request.urlopen(url)
        page = f.read()
        soup = BeautifulSoup(page,"lxml")
        return soup

def find_synonym(word):
    
    url = 'https://de.wiktionary.org/wiki/{}'.format(word)
    soup = get_soup(url)
    
    cond = False
    check = False
    XML = None
    ls_ = []
    startpoint = soup('span', {'id': 'Synonyme'})[0]
    while cond == False:
        
        if check:
            print("Found")
            for s in XML.findall(".//dd/a"):
                ls_.append(s.text)
            
            ls_ = [s for s in ls_ if s is not None]
            return ls_
        
        try:
            XML = ET.fromstring(str(startpoint))
            check = len(XML.findall(".//dd")) != 0
        except:
            pass
                    
        startpoint = startpoint.next_element

def build_lexicon(base_ls):
    
    res = []
    
    for w in base_ls:
    
        try:
            syn_ls = find_synonym(w)
            print("For word :",w)
            print("Synonyms found : ",syn_ls)
            res.extend(syn_ls)
        except:
            print("Issue with word :",w)
            pass
        
    return res

def save_lexicon(ls):
    file = os.path.join(DST_DIR,'de_nouns.pickle')
    res = {'nouns': ls}
    with open(file, 'wb') as f:
        pickle.dump(res, f, protocol=pickle.HIGHEST_PROTOCOL)

# Run
        
def main():
    
    typ = ['Rechnung','Abrechnung','Mietzins','Miete','Zahlung', 'Rückzahlung']
    obj = ['Ferien','Urlaub', 'Teppich', 'Zigarren', 'Geschenk' ,'Elektrizität', 'Heizen', 'Salär', 'Pension',
           'Pensionskasse','2. Säule' ,'Hypothek', 'Ferienwohnung','Wonhnung', 'Haus']
    triv = ['Referenz','ID','Nummer','Nr.']
    
    
    base_ls = typ+obj+triv
    extended_ls = build_lexicon(base_ls)
    print("Size of base lexicon :",len(base_ls))
    print("Size of base lexicon :",len(extended_ls))
    
    save_lexicon(extended_ls)
    print("Lexicon saved")
    
if __name__ == "__main__":
    main()