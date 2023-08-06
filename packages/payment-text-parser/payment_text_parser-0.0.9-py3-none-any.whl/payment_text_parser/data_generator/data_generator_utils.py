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

import numpy as np
import pycountry
import string
import ccy

DE_MONTHS = ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']
DATE_SPLITTERS = ['/','-','']
DATE_FORMATS = ['DATE_FULL','DATE_MONTH_YEAR','DATE_MONTH','DATE_YEAR']

ID_FORMATS = ['ID_IBAN','ID_NUMERIC','ID_NUMERIC_UPPERCASE','ID_NUMERIC_SYMBOL']
COUNTRY_CODES = [c.alpha_2 for c in pycountry.countries]


def generate_date():
    
    split = np.random.choice(DATE_SPLITTERS)
    
    day = np.random.randint(1,32)
    month = np.random.randint(1,13)
    year = np.random.randint(1970,2016)
    
    date_format = np.random.choice(DATE_FORMATS)
    if date_format == 'DATE_FULL':
        n = 2
        ls_ = [str(day).zfill(n),str(month).zfill(n),str(year)]
        res = split.join(ls_)
        return res
    elif date_format == 'DATE_MONTH_YEAR':
        return np.random.choice(DE_MONTHS) + ' ' + str(year)
    elif date_format == 'DATE_MONTH':
        return np.random.choice(DE_MONTHS)
    elif date_format == 'DATE_YEAR':
        return str(year)
        
def generate_id():
    
    id_format = np.random.choice(ID_FORMATS)
    
    if id_format == 'ID_IBAN':
        return np.random.choice(COUNTRY_CODES) + ''.join(np.random.choice(list(string.digits), 20))
    elif id_format == 'ID_NUMERIC':
        n = np.random.randint(1,16)
        return ''.join(np.random.choice(list(string.digits), n))
    elif id_format == 'ID_NUMERIC_UPPERCASE':
        n = np.random.randint(1,16)
        return ''.join(np.random.choice(list(string.ascii_uppercase) + list(string.digits), n))
    elif id_format == 'ID_NUMERIC_SYMBOL':
        n = np.random.randint(1,16)
        base_ls = list(''.join(np.random.choice(list(string.digits), n)))
        SYMBOL_RATIO_MAX = 0.3
        val_high = max(1,round(SYMBOL_RATIO_MAX*n))
        n_replace = np.random.randint(0,val_high+1)

        ind_ls = np.random.choice(range(0, n), n_replace)
        
        for ind in ind_ls:
            symbol = np.random.choice(list(string.punctuation))[0]
            base_ls[ind] = symbol      
        return ''.join(base_ls)
        
def generate_amount():
    
    amount = np.random.randint(1,1e05+1) + round(np.random.random(),2)
    country = np.random.choice(COUNTRY_CODES)
    code = ccy.countryccy(country)
    
    order = np.random.choice(['before','after'])
    if code is not None:
        if order == 'before':
            return code + " " + str(amount)
        elif order == 'after':
            return str(amount) + " " + code 
    else:
        return str(amount)
    
    