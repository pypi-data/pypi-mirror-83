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

import pickle
import re
import pandas as pd
import json
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from faker import Faker
fake = Faker()

from payment_text_parser.data_generator.data_generator_utils import generate_date
from payment_text_parser.data_generator.data_generator_utils import generate_id
from payment_text_parser.data_generator.data_generator_utils import generate_amount

SEED = 4321


#ADDRESS_MIX = {'CH': 0.6, 'en_US': 0.2, 'fr_FR': 0.2}
ADDRESS_MIX = {'CH': 0.4,
               'de_DE':0.1,
               'en_US':0.1,
               'fr_FR':0.1,
               'it_IT':0.1,
               'es_ES':0.15,
               'pt_PT':0.05}
DATA_DIR = os.path.join(HOME_DIR,'data/scraped_data')
TEST_DIR = os.path.join(HOME_DIR,'data/test_data')

# Load data

def get_mixed_ent(entity_type,n_sample=1000,mix={'CH': 1}):
    ls = []

    if entity_type == 'LOC' or entity_type == 'PER':

        for locale, ratio in mix.items():
            if locale != 'CH':
                ls.extend(get_non_swiss_ent(entity_type,n_sample=round(ratio * n_sample),
                                            locale=locale,full_address_only=False))
            else:
                ls.extend(get_swiss_ent(entity_type,n_sample=round(ratio * n_sample)))

    #TODO Find international datasets for ORG
    elif entity_type == 'ORG':
        locale = 'CH'
        ratio = 1
        ls.extend(get_swiss_ent(entity_type, n_sample=round(ratio * n_sample)))

    np.random.shuffle(ls)
    return ls

def get_non_swiss_ent(entity_type,n_sample=1000, locale=None,full_address_only = True):
    fake = Faker(locale)
    fake.seed_instance(SEED)

    if not full_address_only :
        ratio_street = 0.25
        ratio_city = 0.25

    else :
        ratio_street = 0
        ratio_city = 0

    ratio_all = 1 - (ratio_street + ratio_city)

    ls = []

    if entity_type == 'PER':
        for _ in range(n_sample):
            name = fake.name()
            name = name.replace('\n', ' ')
            ls.append(name)

    elif entity_type == 'LOC':
        for _ in range(n_sample):
            opt = np.random.choice(['ALL', 'STREET_ONLY','CITY_ONLY'], p=[ratio_all,ratio_street,ratio_city])
            if opt == 'ALL':
                addr = fake.address()
            elif opt == 'STREET_ONLY':
                addr = fake.address().split('\n')[0]
            elif opt == 'CITY_ONLY':
                addr = fake.address().split('\n')[1]
            addr = addr.replace('\n', ' ')
            ls.append(addr)

    return ls

def get_swiss_ent(entity_type,n_sample=1000):

    if entity_type == 'ORG':
        file = os.path.join(DATA_DIR, 'ORG2.pickle')
        with open(file, 'rb') as f:
            data = pickle.load(f)
            ents = data['individuals']

    if entity_type == 'PER':
        file = os.path.join(DATA_DIR, 'PER.pickle')
        with open(file, 'rb') as f:
            data = pickle.load(f)
            ents = data['individuals']

    elif entity_type == 'LOC':
        file = os.path.join(DATA_DIR, 'PER.pickle')
        with open(file, 'rb') as f:
            data = pickle.load(f)
            ents = data['addresses']

    ls = np.random.choice(ents,n_sample)

    return ls

# Load scraped/generated data

def get_data(entity_type, n_sample):

    if entity_type == 'PER':
        entities = get_mixed_ent(entity_type='PER', n_sample=n_sample, mix=ADDRESS_MIX)

    elif entity_type == 'ORG':
        entities = get_mixed_ent(entity_type='ORG', n_sample=n_sample, mix=ADDRESS_MIX)

    addresses = get_mixed_ent(entity_type='LOC', n_sample=n_sample,mix=ADDRESS_MIX)

    return entities,addresses
 
def get_lexicon():
    
    file = os.path.join(DATA_DIR,'de_nouns.pickle')
    
    with open(file, 'rb') as f:
        data = pickle.load(f)
        lexicon = data['nouns']
    
    return lexicon

# Cleaning

def clean_str(string,pattern):
    
    string_ = re.sub(pattern, '', string)
    string_ = re.sub(' +',' ',string_) # Removes multiple spaces
    res = string_.strip()
    
    return res

def clean_str_ls(string_ls,pattern):
    
    return [clean_str(s,pattern) for s in string_ls]

def label_entity(entity,spacy_label,option='allInOne'):
        if option == 'allInOne':
            l = {entity:spacy_label}
        elif option == 'splitEntities':
            splits = split_entities(entity)
            l = {e:spacy_label for e in splits} 
        return l

def split_entities(string):
    #TODO Complete list
    splits = re.split(' et | und | u. | mit | and | e |,',string)
    return splits   

class GeneratorClass(object):
    
    def __init__(self,n_sample=1000,
                 field_pattern_flavor = 'location_entity_flavor',
                 train_test = {'TRAIN':0.7,'TEST':0.3},
                 field_types = {'ENTITY_ADDRESS':0.5,'FREE_TEXT':0.5}):
        
        # Constants

        #import pdb;pdb.set_trace()
     
        self.n_sample = n_sample
        self.entities_to_split = ['PER']
        self.entities_to_keep = ['PER','ORG','LOC']
        
        self.SPACY_LABELS = {'PER':'PERSON','ORG':'ORG','LOC':'LOC'}
        
        self.FIELD_TYPES = field_types
        self.TRAIN_TEST = train_test

        self.FIELD_COMPONENTS = {
                    'ENTITY_ADDRESS': [
                            ['ENTITY','ADDRESS'],
                            ['ENTITY_PER','ADDRESS','ENTITY_PER','ADDRESS'],
                            ['ENTITY_PER', 'BINDER', 'ENTITY_PER', 'ADDRESS'],
                            ['ENTITY_PER', 'BINDER', 'ENTITY_ORG', 'ADDRESS'],
                            ['ENTITY_ORG', 'BINDER', 'ENTITY_PER', 'ADDRESS'],
                            ['ENTITY_ORG','PART_ADDRESS','BINDER','ENTITY_PER','PART_ADDRESS'],
                            ['ADDRESS', 'ENTITY'],
                            ['ENTITY'],
                            ['ADDRESS']

                    ],
                    'FREE_TEXT' : [
                            ['RATIONALE'],
                            ['RATIONALE','PART_ENTITY'],
                            ['PART_ENTITY','RATIONALE'],
                            ['PART_ENTITY'],
                            ['PART_ADDRESS'],
                            ['RATIONALE','PART_ADDRESS']
                            ]
                    }

        # Weights for field components
        self.FIELD_COMPONENTS_WEIGHTS = {}
        self.FIELD_COMPONENTS_WEIGHTS['ENTITY_ADDRESS'] = [0.35,0.05, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05]
        self.FIELD_COMPONENTS_WEIGHTS['FREE_TEXT'] = [1/6, 1/6, 1/6, 1/6, 1/6, 1/6]

        # Basic pattern
        if field_pattern_flavor == 'location_entity_flavor':
            pass
        # Custom pattern
        elif field_pattern_flavor == 'per_org_flavor':
            self.FIELD_COMPONENTS_WEIGHTS['ENTITY_ADDRESS'] = [0, 0, 1, 0]

        # Plausibility checks
        for fc in ['ENTITY_ADDRESS','FREE_TEXT']:

            len_components = len(self.FIELD_COMPONENTS[fc])
            len_weights = len(self.FIELD_COMPONENTS_WEIGHTS[fc])

            if len_components  != len_weights :
                print("Length mistmach of FIELD_COMPOMENTS_WEIGHTS. Assigning uniform weighting")
                weights = len_components*[1/len_components]
                self.FIELD_COMPONENTS_WEIGHTS[fc] = weights

        self.RATIONALE_BASICS = ['REASON','DATE','ID','AMOUNT']
        self.MY_DUMMY_LABEL = 'DUMMY'
     
        self.ENTITY_TYPES = {'PER':0.3,'ORG':0.7}

        # Mapping components to functions
        
        self.get_component_map = {
                'ENTITY':self.get_entity,
                'ENTITY_PER':self.get_entity_per,
                'ENTITY_ORG': self.get_entity_org,
                'PART_ENTITY': self.get_part_entity,
                'ADDRESS': self.get_address,
                'RATIONALE': self.get_rationale,
                'PART_ADDRESS': self.get_part_address,
                'BINDER':self.get_binder}
        
        self.get_rationale_component_map = {
                'REASON': self.get_lexicon,
                'DATE': generate_date,
                'ID': generate_id,
                'AMOUNT':generate_amount
                }

        # Loading scraped scraping (for individuals and organisations)

        per, addr_per = get_data('PER', n_sample=n_sample)
        org, addr_org = get_data('ORG', n_sample=n_sample)
        addr = addr_per + addr_org

        # Loading lexicon
        
        self.lexicon = get_lexicon()

        # Sampling
        n_per = round(self.ENTITY_TYPES['PER'] * self.n_sample)
        n_org = self.n_sample - n_per
        self.per = np.random.choice(per, n_per)
        self.org = np.random.choice(org, n_org)
        self.addr = np.random.choice(addr, self.n_sample)
        
        # Cleaning
        
        pattern_ = r"\([^\)]*\)" # Removes text between parentheses 
        self.per = clean_str_ls(self.per,pattern_)
    
        pattern_ = r"\," # Removes text between parentheses 
        self.addr = clean_str_ls(self.addr,pattern_)
        
        # Clean for Spacy (remove empty text, map to Spacy labels)
        
        self.CLEAN_FOR_SPACY = True
        
        # Get train/test scraping
        
        self.create_train_test_data()
        
    def generate_pattern(self):

        #import pdb;pdb.set_trace()

        ft = np.random.choice(list(self.FIELD_TYPES.keys()), p=list(self.FIELD_TYPES.values()), size=1)[0]
        fc = np.random.choice(self.FIELD_COMPONENTS[ft],p=self.FIELD_COMPONENTS_WEIGHTS[ft],size=1)[0]
        #fc_ind = np.random.randint(0,len(self.FIELD_COMPONENTS[ft]))
        #fc = self.FIELD_COMPONENTS[ft][fc_ind] #[0]
        
        return ft,fc
    
    def generate_data(self):
        
        data = []
        field_types = []
               
        for i in range(0,self.n_sample):
             
            ft,fc = self.generate_pattern()
            entry,label = self.generate_record(fc)         
            data.append((entry,label))
            field_types.append(ft)
        
        if self.CLEAN_FOR_SPACY:
            data,field_types = self.to_spacy_filter(data,field_types)
        
        return data,field_types
        
    def generate_record(self,components):
        
        entry,label = '',{}      
        
        entry_ls_ = []
        label_ls_ = []
        
        for c in components:
            
            text,ner_label = self.get_component_map[c]() 
            
            entry_ls_.append(text)
            label_ls_.append(ner_label)
        
        entry,label = self.create_record_label(entry_ls_,label_ls_)
          
        return entry,label
      
    def create_record_label(self,entry_ls,label_ls):
        
        res = []
        string = ' '.join(entry_ls)
        
        # Checks if any entity to split
        if len(self.entities_to_split)!=0:

            entry_ls_exploded = []
            label_ls_exploded = []
            
            for substring,sublabel in zip(entry_ls,label_ls):
                if sublabel in self.entities_to_split:
                    # One wants to split PER in pieces
                    entry_ls_exploded.extend(split_entities(substring))
                    n_parts = len(entry_ls_exploded)
                    label_ls_exploded.extend(n_parts*[sublabel])
                else:
                    # Typically, one doesn't want to split ORG in pieces
                    entry_ls_exploded.append(substring)
                    label_ls_exploded.append(sublabel)
            
            entry_ls,label_ls = entry_ls_exploded,label_ls_exploded
        
        for substring,sublabel in zip(entry_ls,label_ls):
            
            if sublabel in self.entities_to_keep:
                ind_start,ind_stop = self.find_indexes(string,substring)
                res.append((ind_start,ind_stop,sublabel))
            else:              
                # Only some labels are relevant for Spacy and are referred in self.entities_to_keep
                pass
        
        entry = string
        label = {"entities":res}
        
        return entry,label
         
    def find_indexes(self,string,substring):
        
        ind_start = string.find(substring)
        ind_stop = ind_start + len(substring)
        
        return ind_start,ind_stop

    def get_entity_per(self):

        return self.get_entity(ner_label = 'PER')

    def get_entity_org(self):

        return self.get_entity(ner_label = 'ORG')

    def get_entity(self,ner_label = None):

        if ner_label is None:
            ner_label = np.random.choice(list(self.ENTITY_TYPES.keys()), p=list(self.ENTITY_TYPES.values()), size=1)[0]
        #ner_label = np.random.choice(list(self.ENTITY_TYPES.keys()),list(self.ENTITY_TYPES.values()),1)[0]
          
        if ner_label == 'PER':
            
            text = np.random.choice(self.per)
            
        elif ner_label == 'ORG':
            
            text = np.random.choice(self.org)
            
        return text,ner_label

    def get_combined_entities(self):

        text1 = self.get_entity()
        text2 = self.get_entity()
        binder = self.get_binder()

        text = " ".join([text1,binder,text2])
        
    def get_address(self):  
         
        text = np.random.choice(self.addr)
        ner_label = 'LOC'
         
        return text,ner_label
      
    def get_part_entity(self):
        
        text,ner_label = self.get_entity()
        
        ratio = np.random.uniform(0.1, 0.7)
        text = self.get_part_text(text,ratio_rmv=ratio)
        
        return text,ner_label
    
    def get_part_address(self):  
         
        text,ner_label = self.get_address()
        ner_label = 'LOC'
        text = self.get_part_text(text)
               
        return text,ner_label   
    
    def get_part_text(self,text,ratio_rmv=0.6):
        
        splits = text.split()
        n_to_remove = round(ratio_rmv*len(splits))
        ind_ls = np.random.choice(range(0,len(splits)),n_to_remove)
            
        text =  " ".join([e for i,e in enumerate(splits) if i not in ind_ls])
        
        return text   

    def get_binder(self):

        ls = ['and','und','et','y','oder','C/O','c/o', '','by','bei']
        text = np.random.choice(ls,1)[0]

        ner_label = 'MISC'

        return text,ner_label

    def get_rationale(self):
        
        n = np.random.choice(range(1,len(self.RATIONALE_BASICS)))
        rationales = np.random.choice(self.RATIONALE_BASICS, n)
        entry_ls_ = []
        
        for r in rationales:
            
            text = self.get_rationale_component_map[r]()         
            entry_ls_.append(text)
        
        text =  ' '.join(entry_ls_)       
        ner_label = self.MY_DUMMY_LABEL
        
        return text,ner_label
    
    def get_lexicon(self):  
         
        text = np.random.choice(self.lexicon)
         
        return text
    
    def to_spacy_filter(self,spacy_tuples,field_types):
        
        spacy_tuples_filter = []
        field_types_filter = []
        
        for t,ft in zip(spacy_tuples,field_types):
            
            text = t[0]          
            # Empty fields  create error in Spacy, we skip
            if text == '':
                continue
            
            # No entity labels, we skip
            if 'entities' not in t[1]:
                continue
            
            # Empty labels, we skip
            label_ls_ = t[1]['entities']
            if len(label_ls_) == 0:
                continue
                       
            label_ls_new_ = []
                  
            for tt in label_ls_:
                if tt[2] in self.SPACY_LABELS:
                    label_ = self.SPACY_LABELS[tt[2]]
                else:
                    # If label not found, we skip this token
                    continue
                tt_new = (tt[0],tt[1],label_)
                label_ls_new_.append(tt_new)                              
                t_new = (text,{'entities': label_ls_new_ }) 

            spacy_tuples_filter.append(t_new)
            field_types_filter.append(ft)
        
        return spacy_tuples_filter,field_types_filter
              
    def to_readable_labels(self,spacy_tuples):
        
        real_labels = {v:k for k,v in self.SPACY_LABELS.items()}
        
        res = []
        for t in spacy_tuples:
            d_ = {}
            text_ = t[0]
            label_ls_ = t[1]['entities']
            for tt in label_ls_:
                ind_start = tt[0]
                ind_stop = tt[1]
                label_ = real_labels[tt[2]]
                d_[text_[ind_start:ind_stop]] = label_
            res.append(json.dumps(d_,ensure_ascii=False))
        return res
            
    def create_train_test_data(self):
        
        data,field_types = self.generate_data()
        
        n_train = round(self.TRAIN_TEST['TRAIN'] * self.n_sample)
        
        self.train_data = data[0:n_train]
        self.test_data = data[n_train:]
        
        self.field_types_train = field_types[0:n_train]
        self.field_types_test = field_types[n_train:]
        
        return self
    
    def get_format_data(self,option='test'):
        
        #import pdb;pdb.set_trace()
        
        if option == 'test':
            data = self.test_data
            field_types = self.field_types_test
        elif option == 'train':
            data = self.train_data
            field_types = self.field_types_train
        
        readable_data = self.to_readable_labels(data)
        
        entities = list(zip(*data))[0]
        labels1 = readable_data
        labels2 = labels1
        
        df = pd.DataFrame(columns=['input','output1','output2'])
        df['input'] = pd.Series(entities)
        df['output1'] = pd.Series(labels1)
        df['output2'] = pd.Series(labels2)
        df['field_type'] = pd.Series(field_types)
        
        return df
    
    def save_data(self,option='test',filename=None):
              
        if option == 'test':
            data = self.test_data
            filename = os.path.join(TEST_DIR,filename)
            df = self.get_format_data(option=option)
        elif option == 'train':
            data = self.train_data
            filename = os.path.join(TEST_DIR,filename)
            df = self.get_format_data(option=option)
        
        if data is not None:
            df.to_csv(filename,sep='|',header=True,index=False)
        
        return self
    
    def make_first_name_counter(self):
        
        def check_pattern(txt):
            pattern = '^[A-Z]+[a-z]+$'
            if re.search(pattern, txt): 
                return True
            else:
                return False
            
        res = []
        for p in self.per:
            try:
                first_names_candidates = p.split()[1:]
                first_names = [f for f in first_names_candidates if check_pattern(f)]
                res.extend(first_names)
            except:
                pass
        return Counter(res)

class NameDictionary():

    def __init__(self):
        
        self.d = {}
         
    def save_data(self):
        
        g = GeneratorClass(n_sample = 100000,train_test = {'TRAIN':0,'TEST':1})
        self.d = g.make_first_name_counter()
        
        file = os.path.join(DATA_DIR,'{}.pickle'.format('first_name'))
    
        with open(file, 'wb') as f:
            pickle.dump(self.d, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    def load_data(self):
        
        file = os.path.join(DATA_DIR,'{}.pickle'.format('first_name'))
        
        with open(file, 'rb') as f:
            d = pickle.load(f)
        
        return d

class TfIdf():

    def __init__(self):

        self.d_tfidf = {}

    def load_data(self):

        file = os.path.join(DATA_DIR, 'tfidf.pickle')

        with open(file, 'rb') as f:
            self.d_tfidf = pickle.load(f)

        self.d_PER = self.d_tfidf['PER']
        self.d_ORG = self.d_tfidf['ORG']

    def make_data(self):

        self.PER_entities,_ = get_data('PER',250000)
        self.ORG_entities,_ = get_data('ORG',250000)

        vectorizer = TfidfVectorizer()
        self.X_PER = vectorizer.fit_transform(self.PER_entities)
        vectorizer = TfidfVectorizer()
        self.X_ORG = vectorizer.fit_transform(self.ORG_entities)
        vectorizer.get_feature_names()

        pattern_ = r"\([^\)]*\)"

        #self.PER_entities = clean_str_ls(self.PER_entities, pattern_)
        #self.ORG_entities = clean_str_ls(self.ORG_entities, pattern_)

        self.create_tfidf()
        self.clean_variables()
        self.create_dict()
        self.save_dict()

    def create_tfidf(self):

        arr = []
        arr.append(' '.join(self.PER_entities))
        arr.append(' '.join(self.ORG_entities))

        self.vectorizer = TfidfVectorizer(ngram_range=(1,2))
        self.X = self.vectorizer.fit_transform(arr)

        return self

    def clean_variables(self):

        del self.PER_entities
        del self.ORG_entities

        return self

    def create_dict(self):

        self.d_PER = dict(zip(self.vectorizer.get_feature_names(),self.X[0].toarray()[0]))
        self.d_ORG = dict(zip(self.vectorizer.get_feature_names(),self.X[1].toarray()[0]))

    def save_dict(self):

        d_tfidf = {}
        d_tfidf['PER'] = self.d_PER
        d_tfidf['ORG'] = self.d_ORG
        file = os.path.join(DATA_DIR, 'tfidf.pickle')

        with open(file, 'wb') as handle:
            pickle.dump(d_tfidf, handle, protocol=pickle.HIGHEST_PROTOCOL)

        return self

    def get_tfidf_score_word(self,word):

        res = [0,0]
        if word in self.d_PER:
            res[0] = self.d_PER[word]
        if word in self.d_ORG:
            res[1] = self.d_ORG[word]

        return res

    def predict_entity(self,text,option = 'sum',
                       tfidf_company_thres = 0,
                       tfidf_comparison_fact_org=1,
                       tfidf_comparison_fact_per=1,
                       stopwords=['and']):

        res = []

        #TODO : Refine exclusion of candidates of tf-idf search like country codes (CH, UK, ..)

        pattern = '|'.join(stopwords)
        w_list = [r.strip() for r in re.split(pattern, text)]
        w_list = [w for w in w_list if len(w) > 2]
        if len(w_list) == 0:
            return 'ND'

        for w in w_list:
            res.append(self.get_tfidf_score_word(w))

        arr = np.array(res)

        if option == 'sum':
            if arr.sum(axis=0).argmax() == 0:
                return 'PER'
            elif arr.sum(axis=0).argmax() == 1:
                return 'ORG'
            else:
                return 'ND'

        elif option == 'any_company':

            # Company threshold
            arr[:, 1] = np.where(arr[:, 1] < tfidf_company_thres, 0, arr[:, 1])
            if any(t == 1 for t in arr.argmax(axis=1)):
                return 'ORG'
            else:
                return 'PER'

        elif option == 'any_company2':

            df = pd.DataFrame(arr)

            checks = []
            for _,row in df.iterrows():

                # True means: is ORG
                if row[0] == 0 and row[1] > tfidf_company_thres:
                    res = 'ORG'
                elif row[0] > 0 and row[1] / row[0] > tfidf_comparison_fact_org:
                    res = 'ORG'
                elif row[1] > 0 and row[0] / row[1] > tfidf_comparison_fact_per:
                    res = 'PER'
                else:
                    res = 'ND'
                checks.append(res)

            if 'ND' in checks:
                final_res = 'ND'
            #else:
            if  'PER' in checks:
                final_res = 'PER'
            if 'ORG' in checks:
                final_res = 'ORG'

            return final_res


if __name__ == '__main__':
    HOME_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    print("Creating tf-idf dictionnary..")
    #tfidf = TfIdf()
    #tfidf.make_data()
    print("Dictionary created.")
    names = NameDictionary()
    names.save_data()
    print("First name dictionary created.")