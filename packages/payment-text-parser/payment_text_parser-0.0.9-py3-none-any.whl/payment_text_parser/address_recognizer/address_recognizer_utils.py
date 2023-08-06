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

import os
import sys

HOME_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, HOME_DIR)

from postal.parser import parse_address
from payment_text_parser.entity_extractor.spacy_models import SpacyModels
import spacy
from collections import Counter
import re

import os
import corenlp
os.environ["CORENLP_HOME"] = r'../core_nlp/stanford-corenlp-full-2018-10-05/'

# Load spacy_models

#if not 'spacy_models' in locals():
#    spacy_models = SpacyModels()

#nlp = spacy_models.spacy_models['XX']
# nlp = spacy.load('de_core_news_sm')
nlp = spacy.load(os.path.join(HOME_DIR, 'models/spacy_models/custom_de_core_news_sm_LOC-ENT_100000_0_0.0.72'))

# Simple tag extraction for flat input ['house','postcode','NOUN','PROPN']

def _clean_libpostal_tag(text):
    
    return text.replace("_","").upper()  

def _get_libpostal_tag_seq(text):
    
    #return [clean_libpostal_tag(t[1]) for t in parse_address(text)]
    return [t[1] for t in parse_address(text)]
    #return ['LIBPOSTAL']

def get_corenlp_token(text):
    
    ls = []
    annotators = 'pos'
    
    client = corenlp.CoreNLPClient(annotators=annotators.split())
    
    try:
        client.is_alive()
        ann = client.annotate(text)
        
        for s in ann.sentence:
            for tkn in s.token:
                #ls.append((tkn.word,tkn.pos))
                ls.append(tkn)  
        return ls
    
    except:  
        print("CoreNLP server not responding. Moving out without tags")
        #sys.exit('sys exit')
        ls = []
    
    return ls

  
def _get_nlp_tag_seq(text,lib = 'spacy'):
    
    if lib == 'spacy':
        return [token.pos_ for token in nlp(text)]
    elif lib == 'corenlp':
        return [token.pos for token in get_corenlp_token(text)]
    #return ['SPACY']     
    
def _get_corenlp_tuple_seq(text):
    
    ls = []
    annotators = 'pos'
    
    with corenlp.CoreNLPClient(annotators=annotators.split()) as client:
        ann = client.annotate(text)
        
    for s in ann.sentence:
        for tkn in s.token:
            #ls.append((tkn.word,tkn.pos))
            ls.append(tkn.pos)
            
    return ls    

def _get_tag_seq(text):
    
    #return _get_libpostal_tag_seq(text) + _get_nlp_tag_seq(text)
    return _get_libpostal_tag_seq(text) + _get_nlp_tag_seq(text,lib = 'corenlp')
    #return _get_libpostal_tag_seq(text) + _get_nlp_tag_seq(text,lib = 'spacy')
    #return _get_nlp_tag_seq(text,lib = 'spacy')
    #return _get_nlp_tag_seq(text,lib = 'corenlp')
    
def get_concatenated_tag_text(text):
 
    return ' '.join(_get_tag_seq(text))

# Combine libpostal and spacy for 1D input ['house_NOUN','postcode'_PROPN']

def _get_libpostal_tuple_flat_seq(text):
    
    libpostal_seq = parse_address(text)

    res = [] 
    for tpl in libpostal_seq:
        
        text = tpl[0]
        label = tpl[1]       
        words = text.split(' ')
        
        for w in words:           
            res.append((w,label))
            
    return res

def get_nlp_tuple_seq(text,lib='spacy'):
    
    if lib == 'spacy':
        return [(token.text.lower(),token.pos_) for token in nlp(text)]
    elif lib == 'corenlp':
        return [(token.word.lower(),token.pos) for token in get_corenlp_token(text)]
 
def combine_seq(seq1,seq2):
    
    res = []    
    for t1,t2 in zip(seq1,seq2):
        
        if t1[0] == t2[0]:
            res.append(t1[1]+'_'+t2[1])
        else:
            pass
    
    return res

def combine_seq2(seq1,seq2): # Also gives text
    
    res = []    
    for t1,t2 in zip(seq1,seq2):
        
        if t1[0] == t2[0]:
            res.append((t1[0],t1[1]+'_'+t2[1]))
        else:
            pass
    
    return res
        
def get_combined_tag_text(text):
    
    seq1 = _get_libpostal_tuple_flat_seq(text)
    seq2 = get_nlp_tuple_seq(text,lib='corenlp')
    
    res_seq = combine_seq(seq1,seq2)
    
    return ' '.join(res_seq)

# Add libpostal token length
    
def get_libpostal_tag_length(text):
    
    seq = parse_address(text)
    res = []
    for t in seq:
        length = len(t[0])
        tag = t[1]
        res.append((tag+"_len",length))
    
    return dict(res)      

# Add combined token length
 
def get_combined_tag_length(text):

    seq1 = _get_libpostal_tuple_flat_seq(text)
    seq2 = get_nlp_tuple_seq(text,lib='corenlp')
    
    # Removing PUNCT token since ignored by libpostal
    seq2 = [t2 for t2 in seq2 if t2[1] != 'PUNCT'] 
    
    # Combining both lists
    res = []    
    for t1,t2 in zip(seq1,seq2):
            
        if t1[0] == t2[0]:
            length = len(t1[0])
            combined_tag = t1[1]+'_'+t2[1]
            res.append((combined_tag,length))
        else:
            pass
    
    # Conversion list of tuple => dict, creating new keys for dupplicates
    d = {}
    dupplicated_keys_nb = Counter()
    for t in res:
        k = t[0]
        v = t[1]
        if k not in d:
            d[k] = v
        else:
            dupplicated_keys_nb[k] += 1
            d[k+'_'+ str(dupplicated_keys_nb[k])] = v          
            
    return d

# Heuristics
    
def check_code(text):

    return bool(re.match('^(?=.*[0-9])(?=.*[a-zA-Z])', text))



