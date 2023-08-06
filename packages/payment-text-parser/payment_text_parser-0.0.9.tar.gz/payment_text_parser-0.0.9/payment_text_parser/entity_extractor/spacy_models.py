#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 19:37:00 2019

@author: Pierre
"""
import os
import sys
HOME_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, HOME_DIR)

import operator

os.environ["CORENLP_HOME"] = r'./corenlp/stanford-corenlp-full-2018-10-05/'

import spacy
# Install package: python -m spacy download de_core_web_md
#nlp = spacy.load('en')
#nlp = spacy.load('xx_ent_wiki_sm')
#nlp = spacy.load('de')
#nlp = spacy.load('de_core_news_sm')

#modulename = 'de_core_news_md'
#if modulename not in sys.modules:

from langdetect import detect 

class SpacyModels(object):
    
    def __init__(self):
        
        self.LANGUAGES = ['EN','DE']
        
        #print("Loading Spacy model..")
        
        self.models= {}
        
        # Custom spacy_models trained on mix

        # self.models['ENTITY_ADDRESS'] = {
        #         'DE': spacy.load(os.path.join(HOME_DIR,'models/spacy_models/custom_de_core_news_sm_100_address_0.5')),
        #         'XX': spacy.load(os.path.join(HOME_DIR,'models/spacy_models/custom_de_core_news_sm_100_address_0.5'))
        #         }
        #
        # self.models['FREE_TEXT'] = {
        #         'DE': spacy.load(os.path.join(HOME_DIR,'models/spacy_models/custom_de_core_news_sm_100_address_0.5')),
        #         'XX': spacy.load(os.path.join(HOME_DIR,'models/spacy_models/custom_de_core_news_sm_100_address_0.5'))
        # }

        # Custom spacy_models trained on mix

        LOC_ENT_model = 'models/spacy_models/custom_de_core_news_sm_LOC-ENT_100000_1_0.0.72'
        #LOC_ENT_model = 'models/spacy_models/custom_de_core_news_sm_LOC-ENT_100000_1_0.0.71'
        #LOC_ENT_model = 'models/spacy_models/custom_de_core_news_sm_LOC-ENT_100000_1_0.0.70'
        #LOC_ENT_model = 'models/spacy_models/custom_de_core_news_sm_LOC-ENT_100000_1_0.0.69'
        #LOC_ENT_model = 'models/spacy_models/custom_de_core_news_sm_LOC-ENT_100000_1_0.0.67'
        #LOC_ENT_model = 'models/spacy_models/custom_de_core_news_sm_LOC-ENT_10000_1_v0003'
        PER_ORG_model = LOC_ENT_model
        #LOC_ENT_model = 'models/spacy_models/custom_de_core_news_sm_LOC-ENT_100000_0.7_v0001'
        #LOC_ENT_model = 'models/spacy_models/custom_de_core_news_sm_100000_address_0.5_spacy1.x'
        FREE_TEXT_model = 'models/spacy_models/custom_de_core_news_sm_LOC-ENT_100000_0_0.0.72'

        self.models['ENTITY_ADDRESS'] = {}
        self.models['ENTITY_ADDRESS']['LOC_ENTITY'] = {
            'DE': spacy.load(os.path.join(HOME_DIR, LOC_ENT_model)),
            'XX': spacy.load(os.path.join(HOME_DIR, LOC_ENT_model))
        }
        self.models['ENTITY_ADDRESS']['PER_ORG'] = {
            'DE': spacy.load(os.path.join(HOME_DIR, PER_ORG_model)),
            'XX': spacy.load(os.path.join(HOME_DIR, PER_ORG_model))
        }

        self.models['FREE_TEXT'] = {}
        self.models['FREE_TEXT']['LOC_ENTITY'] = {
            'DE': spacy.load(os.path.join(HOME_DIR, FREE_TEXT_model)),
            'XX': spacy.load(os.path.join(HOME_DIR, FREE_TEXT_model))
        }
        self.models['FREE_TEXT']['PER_ORG'] = {
            'DE': spacy.load(os.path.join(HOME_DIR, FREE_TEXT_model)),
            'XX': spacy.load(os.path.join(HOME_DIR, FREE_TEXT_model))
        }
              
        # Standard spacy_models
        
        """
        self.models['ENTITY_ADDRESS'] = {
                'DE': spacy.load(os.path.join('de_core_news_sm')),
                'XX': spacy.load(os.path.join('de_core_news_sm'))
                }
    
        self.models['FREE_TEXT'] = {
                'DE': spacy.load(os.path.join('de_core_news_sm')),
                'XX': spacy.load(os.path.join('de_core_news_sm')),
                }
        """
        
        self.vocs = {}
        for entity_type,d1 in self.models.items():
            self.vocs[entity_type] = {}
            for model_flavor,d2 in d1.items():
                self.vocs[entity_type][model_flavor] = {}
                for lan, model in d2.items():
                    self.vocs[entity_type][model_flavor][lan] = list(model.vocab.strings)
        
        print("Models loaded")
     
    def detect_language(self,text):
        
        language = detect(text).upper()
        if language not in self.LANGUAGES:
            language = 'XX'      
        return language
        
    def detect_language2(self,text):
        
        probs = {}
        for language,nlp in self.models.items():
            doc = nlp(text)
            prob = sum(tok.prob for tok in doc)
            probs[language] = prob
        
        best_language = max(probs.items(), key=operator.itemgetter(1))[0]
        return best_language