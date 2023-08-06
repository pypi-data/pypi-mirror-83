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

import corenlp
import os
import difflib
import re
import pandas as pd

os.environ["CORENLP_HOME"] = r'./corenlp/stanford-corenlp-full-2018-10-05/'

from names_dataset import NameDataset
from collections import defaultdict
from difflib import SequenceMatcher

import pycountry
COUNTRY_CODES = [c.alpha_2 for c in pycountry.countries]

PERSON_LABEL = 'PER'

# Text processing

def pypostal_tc(text_tc,parsed_list_lc):

    parsed_list_tc = []
    
    # Iterates over tuples
    for tuple_lc in parsed_list_lc:
        
        substr_tc = ''
        substr_lc = tuple_lc[0]
        
        # Iterates over words in tuple sub-string
        for w_lc in substr_lc.split():
                  
            ind_start = text_tc.lower().find(w_lc)
            ind_stop = ind_start + len(w_lc)
            w_tc = text_tc[ind_start:ind_stop]
            substr_tc += w_tc + ' '
            
            text_tc = text_tc[ind_stop:] # Removes substring
         
        substr_tc = substr_tc.rstrip()
        tuple_tc = (substr_tc,tuple_lc[1])
            
        parsed_list_tc.append(tuple_tc)
            
    return parsed_list_tc

def true_case(text,option='corenlp',org_acronyms=[],per_acronyms=[]):
    
    if option == 'corenlp':
        
        annotators = "truecase"
        with corenlp.CoreNLPClient(annotators=annotators.split()) as client:
          ann = client.annotate(text)

        ls_ = []
        for s in ann.sentence:
            for tkn in s.token:
                ls_.append(tkn.trueCaseText)
        truecase_text = ' '.join(ls_)

    elif option == 'naive':

        res = ''
        sc = [',','-','.'] # Special characters to ignore (e.g. to get 'HOUSE,' as 'House,')

        for w in text.split():
        #for w in re.findall(r"[\w']+", text):
            w_cl = ''.join([c for c in w if c not in sc])
            if w_cl in org_acronyms:
                w_ = w
            elif '-' in text: # To capitalize JEAN-PIERRE as Jean-Pierre
                w_ = '-'.join([ww.capitalize() for ww in w.split('-')])
            elif w in COUNTRY_CODES:
                w_ = w
            elif w_cl in per_acronyms:
                w_ = w.capitalize()
            else:
                if w.isalpha():
                    w_ = w.capitalize()
                else:
                    w_ = w
            res += ' '+w_

        truecase_text = res.strip()

    return truecase_text
    
def flag_first_last_name(text):
    
    d = {}

    for w in text.split():
        d[w] = []
        m = NameDataset()
        if m.search_first_name(w):
            d[w].append('FIRST')
        if m.search_last_name(w):
            d[w].append('LAST')
    
    return d

def normalize_label(label):
    if label == 'PERSON':
        return PERSON_LABEL
    else:
        return label

def categorize_ent(label):
    if 'LOC' not in label and ('ORG' in label or 'PER' in label):
        return 'ENT'
    else:
        return label
    
def hasNumbers(inputString):
    
    return any(char.isdigit() for char in inputString)

def dict_diff(d1,d2):
    
    return { k : d2[k] for k in set(d2) - set(d1) }

def reverse_dict(d):
    d_inv = defaultdict(list)
    for k, v in d.items():
        d_inv[v].append(k)

    d_res = {}
    for k, v in d_inv.items():
        d_res[k] = ' '.join(d_inv[k])

    return d_res

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def find_duplicates(ls):
    seen = set()
    uniq = []
    duppl = []
    for x in ls:
        if x not in seen:
            uniq.append(x)
            seen.add(x)
        else:
            duppl.append(x)
    return duppl

def create_d_loc(d):
    d_ = {}
    for k,v in d.items():
        if v.islower():
            d_[k] = 'LOC'
    return d_

def remove_last_dot(w):
    if w[-1] == '.' :
        w = w[0:-1]
    return w

def get_matches(string1,string2):
    matches = difflib.SequenceMatcher(
        None, string1, string2).get_matching_blocks()
    return matches

def find_best_lowercase_match(string_input, list_input):
    string_input_lower = string_input.lower()
    list_input_lower = [l.lower() for l in list_input]
    #res = difflib.get_close_matches(string_input_lower, list_input_lower, n=1)
    #res_ls = difflib.get_close_matches(string_input_lower, list_input_lower, len(list_input_lower),0)
    s = string_input_lower
    res_ls = [l for l in list_input_lower if (s in l or l in s) and (len(s) > 3)]

    if len(res_ls) == 1:
        res = res_ls[0]
        return [x for x in list_input if x.lower() in res]
    else:
        return []

def clean_stopwords(d,stopwords=[]):
    #import pdb;pdb.set_trace()
    d_ = d.copy()
    for k,v in d.items():
        k_lower = k.lower()
        ls_ = k_lower.split()
        for s in stopwords:
            if s in ls_:
                if ls_.index(s) == 0 or ls_.index(s) == len(ls_)-1:
                    del d_[k]
                    k_new = k.replace(s,'').strip()
                    d_[k_new] = v
    return d_

# Cleaning duplicates

def get_min_pos_text(d_addr, to_investigate_tags, text_ls):
    df_check = get_text_tag_pos_df(d_addr, text_ls)
    ls = []
    for tag in to_investigate_tags:
        df_tag = df_check[df_check['tag']==tag]

        # If case same tag appears multiple times on same element of text_ls
        if True in df_tag['pos'].duplicated().tolist():
            #k_addr = df_tag.loc[df_tag['pos'].idxmin()]['text']
            for pos in df_tag['pos'][df_tag['pos'].duplicated()]:
                df_tag_pos = df_tag[df_tag['pos']==pos]
                d_ = {}
                for t in df_tag_pos['text'].tolist():
                    text = text_ls[pos]
                    ind = text.index(t)
                    d_[t] = ind
            k_addr = min(d_, key=d_.get)

        # If tag appears on different element of text_ls
        else:
            k_addr = df_tag.loc[df_tag['pos'].idxmin()]['text']

        #d_duppl = get_min_pos_dict(tag=tag, d_addr=d_addr, ls=text_ls)
        #k_addr = min(d_duppl, key=d_duppl.get)
        ls.append(k_addr)
    return ls

def get_min_pos_dict(tag, d_addr, ls):
    d = {}
    for k, v in d_addr.items():
        if v == tag:
            d[k] = get_pos(k, ls,option='naive', selection ='min')
    return d

def get_pos_dict(tag, d_addr, ls):
    d = {}
    for k, v in d_addr.items():
        if v == tag:
            d[k] = get_pos(k, ls,option='naive', selection ='all')
    return d

def get_pos(text1, text2_ls, option='naive', selection ='all'):
    t1_lower = text1.lower()

    ind_ls = []

    if option == 'naive':
        for ind, text2_real in enumerate(text2_ls):
            t2_lower = text2_real.lower()
            if (t1_lower in t2_lower) or (t2_lower in t1_lower):
                ind_ls.append(ind)
    else:
        pass

    if len(ind_ls)>0 and selection == 'min':
        return min(ind_ls)
    else:
        return ind_ls

# Order plausiblity checks

def get_text_tag_pos_df(d, ls):

    res = []

    for k, tag in d.items():
        for pos in get_pos(k, ls, option='naive', selection='all'):
            d_ = {}
            d_['text'] = k
            d_['tag'] = tag
            d_['pos'] = pos
            res.append(d_)

    #  Appends
    df = pd.DataFrame(res)

    return df

def check_order(t, df):
    res = []
    order_check = []
    #df = df.sort_values(by='pos')

    for tag in t:
        order_check.extend(df[df['tag']==tag]['pos'].tolist())

    """
    for n in range(0, df.shape[0]):
        df_sub = df.loc[0:n, :]
        order_check = []
        for tag in t:
            order_check.append(get_min_pos(tag, df_sub))
    """

    candidate_check = [e for e in order_check if e is not None]
    order_check = candidate_check.copy()
    order_check.sort()

    if order_check == []:
        res.append(True)
    elif candidate_check == order_check:
        res.append(True)
    else:
        res.append(False)

    return res

def get_min_pos(tag, df):
    df_tag = df[df['tag'] == tag]
    if df_tag.shape[0] > 0:
        return min(df_tag['pos'])
    else:
        return None
