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
import re
import sys
import unidecode
import pycountry
from collections import defaultdict
from collections import OrderedDict

from payment_text_parser.data_generator.data_generator import TfIdf
from payment_text_parser.data_generator.data_generator import NameDictionary
from payment_text_parser.entity_extractor.entity_extractor_utils import *
from payment_text_parser.entity_extractor.spacy_models import SpacyModels
from names_dataset import NameDataset
from postal.parser import parse_address

from payment_text_parser.address_recognizer.address_recognizer_utils import combine_seq2
from payment_text_parser.address_recognizer.address_recognizer_utils import get_nlp_tuple_seq

# Class instantiations

spacy_models = SpacyModels()
models = spacy_models.models
vocs = spacy_models.vocs

namedataset = NameDataset()  # From external library
namedictionary = NameDictionary()  # From current library


# Enable if needed
ENABLE_RECOGNIZER = False
if ENABLE_RECOGNIZER:
    from payment_text_parser.address_recognizer.address_recognizer import Recognizer
    recognizer = Recognizer('concat', sample_size=10)
    recognizer.load_model()

# Load tf-idf scores

tfidf = TfIdf()
tfidf.load_data()

# Creates first names dictionaries

d_first_names_1 = namedictionary.load_data()
d_first_names_2 = dict.fromkeys(namedataset.last_names,0)  # We put a freq of 0 since not available

d_first_names = d_first_names_1
#  d_first_names = {**d_first_names_1,**d_first_names_2}
d_first_names = {k.lower():v for k,v in d_first_names.items()}

COUNTRY_CODES = [c.alpha_2 for c in pycountry.countries]

# Class definition

class ExtractorClass(object):

    def __init__(self, text, language='XX', field_type='ENTITY_ADDRESS',
                 pos_library='corenlp', confidence_spacy='high', check_true_case=True, check_language=False,
                 check_field_type=False, check_payment_standard = False, check_tfidf = False, check_acronyms_per=True, check_acronyms_org=True, check_first_name=False,
                 check_regex=True, check_spacy_confidence=True, check_heuristics_tuning=True,
                 create_parsed_address=True, create_nlp_tags_rest_text=False, create_nlp_tags_full_text=False,
                 custom_tech_words = ['MIST']):
        
        # Raw input

        self.text = text
        self.text_raw = self.text
        self.text_remaining = self.text

        # NLP Parameters

        self.language = language
        self.field_type = field_type
        self.pos_library = pos_library
        self.confidence_spacy = confidence_spacy

        # Tuning parameters

        self.FIRST_NAME_MIN_LEN = 3
        self.SPACY_CONFIDENCE_PER = 0.99
        self.SPACY_CONFIDENCE_ORG = 1
        self.ENTITY_PLAUSIBILITY_THRESHOLD = 0.5
        self.NB_MIN_ADDRESS_FIELDS = 1
        self.TRUE_CASE_METHOD = 'naive'
        self.MINIMAL_NB_SUBFIELDS = 3 # Now warning if nb subfields >= 3
        self.ADDRESS_PLAUSIBILITY_THRESHOLD = 0.5
        self.ADJACENT_ENTITIES = False #Forces to find adjacent entities
        self.iteration_nb = 0

        # Postal flags that might be entities

        self.MAIN_ENTITY_MAIN_IND = 2 # Main entity should be on indexes 0,1 or 2 max
        self.MATCH_SIZE = 5
        self.TFIDF_COMPANY_THRES = 1e-04
        self.TFIDF_COMPARISON_FACT_ORG = 50
        self.TFIDF_COMPARISON_FACT_PER = 2
        self.ADJACENT_ENTITIES_TOL = 5
        self.CLEANING_CANDIDATES = [',']
        self.MAIN_SPLITTER_CANDIDATES = ['@', "\n\r","\r\n","\n"] + ["C/O" , "c/o", "C/o", "und/oder", "ET/OU", "U/O","oder"]
        self.ENT_SPLITTER_CANDIDATES = ["/"]
        self.LOC_SPLITTER_CANDIDATES = [] #["."]

        self.STOPWORDS_SYM = ['\s+', '\+', '\&', '\-']
        self.STOPWORDS_ACR = ['and ', 'und ', 'et ', 'i ', 'y ']
        self.STOPWORDS_ACR += [s.capitalize() for s in self.STOPWORDS_ACR] + [s.upper() for s in self.STOPWORDS_ACR]
        self.STOPWORDS = self.STOPWORDS_SYM + self.STOPWORDS_ACR

        self.ORG_ACRONYMS = ['AG', 'A.G.', 'GmbH', 'Gmbh',
         'SA', 'S.A', 'S.A.R.L', 'S.A.R.I', 'Sàrl', 'SARL','SARI','Sagl', 'SAGL',
         'LTD', 'Ltd', 'ltd', 'LLC', 'Llc', 'llc', 'INC', 'S.P.A']

        self.PER_ACRONYMS = ['M','Me','Mme', 'Monsieur', 'Madame', 'Herr', 'Frau', 'Mr', 'Mrs', 'Dr', 'med',
         'M', 'MME', 'MONSIEUR', 'MADAME', 'HERR', 'FRAU', 'MR', 'MRS', 'DR', 'MED']

        self.CUSTOM_TEC_WORDS = custom_tech_words
        self.MINIMUM_REQUIRED_FIELD_LIBPOSTAL = ['city','country','state_district']
        self.POSTAL_ENTITY_MIN_LENGTH_TO_RETRY_ON_SPACY = 2
        self.NOT_SUFFICIENT_TAGS = [['house','city']]

        self.TOLERATED_SEQ = [['road','city'],['city','country'],['road','city','LOC'],['house','city'],['ENT','city'],['ENT','city','LOC']] # LOC comes from d_rest

        # Constants

        self.TAG_NADDR = 'naddr'
        self.TAG_NER = 'ner'

        # Heuristics parameters

        self.check_true_case = check_true_case
        self.check_language = check_language
        self.check_field_type = check_field_type
        self.check_payment_standard = check_payment_standard
        self.check_tfidf = check_tfidf
        self.check_acronyms_per = check_acronyms_per
        self.check_acronyms_org = check_acronyms_org
        self.check_first_name = check_first_name
        self.check_regex = check_regex
        self.check_spacy_confidence = check_spacy_confidence
        self.check_heuristics_tuning = check_heuristics_tuning

        if self.check_payment_standard:
            self.ADJACENT_ENTITIES = True

        # Postprocessing parameters

        self.create_parsed_address = create_parsed_address
        self.create_nlp_tags_rest_text = create_nlp_tags_rest_text
        self.create_nlp_tags_full_text = create_nlp_tags_full_text

        # Initialization indicator values

        self.has_true_case_used = False
        self.has_tfidf_changed = False
        self.has_acronym_org = False 
        self.has_acronym_per = False 
        self.has_first_name = False
        self.has_regex = False
        self.has_low_spacy_confidence = False
        self.has_heuristics_tuning = False
        self.has_plausible_main_entity = False
        self.has_plausible_address = False

        # Variables

        self.text_addr = ''
        self.text_naddr = ''
        self.text_ner = ''
        self.text_rest = self.text
        self.text_buffer = ''
        self.text_buffer2 = ''
        self.text_country_code = ''

        self.text_ls = []
        self.text_ls_raw = []
        self.text_ls_remaining = []

        self.nlp_tags_ner = []
        self.nlp_tags = []

        self.diff_neg_ls = []
        self.diff_pos_ls = []

        #self.d_ner = {}
        #self.d_loc_spacy = {}
        #self.d_addr = {}
        #self.d_rest = {}

        self.d_ner = OrderedDict()
        self.d_loc_spacy = OrderedDict()
        self.d_addr = OrderedDict()
        self.d_rest = OrderedDict()
        self.d_warn = OrderedDict()

        self.entity_scores = {}

        #import pdb;pdb.set_trace()
        self.recursion = 0
        self.ignore_entity_plausibility_check_structure = False

        # Pre-processing

        if self.check_payment_standard:
            self.swift_cleaning()
            self.swift_splitting()
            self.swift_regex_identification()

        # In case no splitter is searched/found
        if len(self.text_ls) == 0:
            self.text_ls_raw.append(self.text_raw)
            self.text_ls.append(self.text)
            self.text_ls_remaining = self.text_ls

        # Options

        if self.check_true_case:
            self.true_case()
            if self.text_raw.isupper():
                pass #self.true_case()
            else:
                pass

        if self.check_language:
            try:
                self.language = spacy_models.detect_language(self.text)
            except:
                pass
        
        if self.check_field_type:
            try:
                self.detect_field_type()
            except:
                pass

        # Checking if there is a model for language found
        if self.language not in models[self.field_type]:
            self.language = 'XX'
         
        # Picks model
        self.nlp = models[self.field_type]['LOC_ENTITY'][self.language]
        self.voc = vocs[self.field_type]['LOC_ENTITY'][self.language]

        # Processing

        self.iteration_nb = 0

        self.extract_ner()

        if self.create_parsed_address:
            self.extract_addr()
        else:
            pass

        if self.check_payment_standard: #Makes a second round with buffered elements (i.e. not matching payment structure)

            self.iteration_nb = 1
            self.ignore_entity_plausibility_check_structure = True # No structural check now on buffered text
            self.extract_addr(text=self.text_buffer)
            self.extract_ner(text=self.text_buffer)

        # Heuristic application

        ## Part 1 : additional checks
        if check_regex:
            self.regex_filter()
        if self.check_tfidf:
            self.tfidf_filter()
        if check_first_name:
            self.first_name_filter()
        if check_spacy_confidence:
            self.spacy_confidence_filter()
        if check_heuristics_tuning:
            self.heuristics_tuning()

        ## Part 2 : acronyms are enough to decide
        if self.check_acronyms_org:
            self.acronym_filter(filter_type='ORG')
        if self.check_acronyms_per:
            self.acronym_filter(filter_type='PER')

        # Plausibility
        if check_payment_standard:
            self.address_plausibility_check()
            if not self.has_plausible_address:
                #self.d_addr =  {'NOT ENOUGH ADDRESS FIELDS':'WARN04'}
                self.d_loc_spacy = self.d_addr
            self.cleaning_postprocessing()
            self.order_plausibility_check()

        # Separate post-processing (i.e. not given in d_res)

        if self.create_nlp_tags_rest_text:
            self.extract_rest()
        else:
            pass

        if self.create_nlp_tags_full_text:
            self.create_nlp_indicators()
        else:
            pass


    # Final result : dictionary containing entities, addresses and nlp tags

    @property
    def d_loc(self):
        # Merge locations from Libpostal into 'LOC'
        return create_d_loc(self.d_addr)

    @property
    def d_res(self):
        # Detailed result with NER, locations from Libpostal, NLP tags on rest and errors
        return {**self.d_ner, **self.d_addr, **self.d_rest, **self.d_warn}

    @property
    def d_res2(self):
        # Simple result with NER, merged locations and errors
        return {**self.d_ner, **self.d_loc, **self.d_rest, **self.d_warn}

    @property
    def POSTAL_ENTITY_TAGS_TOLERATED_IN_SPACY(self):

        if self.iteration_nb == 0:
            return ['house']
        else:
            return ['house','road','state_district']

    @property
    def POSTAL_ENTITY_TAGS_TO_RETRY_ON_SPACY(self):

        if self.iteration_nb == 0:
            if not self.has_plausible_main_entity:
                return ['house','road','state_district','suburb']
            else:
                return ['house','road','state_district','suburb']
        else:
            if not self.has_plausible_main_entity:
                return ['house','road','state_district','suburb']
            else:
                return ['house','road','state_district','suburb']

    @property
    def POSTAL_ENTITY_DUPLICATED_TAGS_TO_RETRY_ON_SPACY(self):

        return self.POSTAL_ENTITY_TAGS_TO_RETRY_ON_SPACY + ['road','city','country']

    @property
    def POSTAL_ENTITY_DUPLICATED_TO_TREAT_AS_ENT(self):

        return ['city', 'country','road']

    @property
    def POSTAL_ENTITY_FIRST_LINE_TO_TREAT_AS_ENT(self):

        return ['city','state','country','road','house']


    # Methods

    def swift_cleaning(self):

        for s in self.CLEANING_CANDIDATES:
            self.text = self.text.replace(s, ' ')
        self.text = self.text.strip()

    def swift_splitting(self):

        # Main splitter

        pattern = '|'.join(self.MAIN_SPLITTER_CANDIDATES)
        self.text_ls_raw = [r.strip() for r in re.split(pattern, self.text_raw)]
        self.text_ls_raw = [r for r in self.text_ls_raw if len(r) > 0 ]
        self.text_ls = [r.strip() for r in re.split(pattern, self.text)]
        self.text_ls = [r for r in self.text_ls if len(r) > 0 ]
        self.text = ' '.join(self.text_ls)

        if len(self.text_ls) < 3:
            self.d_warn = {**self.d_warn, **{'NB OF SUBFIELDS LOWER THAN {}'.format(self.MINIMAL_NB_SUBFIELDS): 'WARN01'}}

    def swift_regex_identification(self):

        self.text_remaining = self.text
        self.text_ls_remaining = self.text_ls

        ls_ = self.text_ls_remaining.copy()

        for s in ls_:
        #for s in self.text_ls_remaining:

            # Account pattern
            account_regex = re.compile('[/0-9]{6,}')
            #account_regex = re.compile("^([\/]*([A-Z]{2})*[0-9]{6,})$")
            if s in self.text_ls_remaining and ' ' not in s and account_regex.search(s) is not None:
                self.d_rest[s] = 'ACC'
                self.text_ls_remaining.remove(s)
                self.text_remaining = self.text_remaining.replace(s,'').strip()

            # Country code
            if s in self.text_ls_remaining and len(s) == 2 and s.isalpha() :
                self.text_ls_remaining.remove(s)
                self.text_remaining = ' '.join(self.text_ls_remaining)
                self.text_country_code = s
                self.d_addr[s] = 'country_code'

            # Trivial words alone (Herr or Monsieur alone on a line)
            if s in self.text_ls_remaining and remove_last_dot(s) in self.PER_ACRONYMS:
                self.text_ls_remaining.remove(s)
                self.text_remaining = ' '.join(self.text_ls_remaining)

            # Technical pattern
            technical_regex = re.compile('^[A-Z]+[\/][A-Z]+$')
            if s in self.text_ls_remaining and technical_regex.search(s) is not None:
                self.d_rest[s] = 'TEC'
                #if self.text_ls_remaining.index(s) > self.MAIN_ENTITY_MAIN_IND:
                self.text_ls_remaining.remove(s)
                self.text_remaining = self.text_remaining.replace(s,'').strip()

            # Custom words
            if s in self.text_ls_remaining and s in self.CUSTOM_TEC_WORDS:
                self.d_rest[s] = 'TEC'
                #if self.text_ls_remaining.index(s) > self.MAIN_ENTITY_MAIN_IND:
                self.text_ls_remaining.remove(s)
                self.text_remaining = self.text_remaining.replace(s, '').strip()

        return self

    def true_case(self):

        try:
            text_tc = true_case(self.text_remaining,option=self.TRUE_CASE_METHOD,org_acronyms=self.ORG_ACRONYMS,per_acronyms=self.PER_ACRONYMS)
            text_ls_tc = [true_case(t_,option=self.TRUE_CASE_METHOD,org_acronyms=self.ORG_ACRONYMS,per_acronyms=self.PER_ACRONYMS) for t_ in self.text_ls_remaining]
            if text_tc != self.text:
                self.has_true_case_used = True
            else:
                self.has_true_case_used = False

            self.text_remaining = text_tc
            self.text_ls_remaining = text_ls_tc

        except:
            pass

    def extract_ner(self,text=None):

        if self.iteration_nb == 0:
            self.text_rest = self.text_remaining

        # Parsing entity fields using spacy

        if text is None:
            text = self.text_remaining

        # Removing secondary splitters
        for s in self.ENT_SPLITTER_CANDIDATES:
            text = text.replace(s,' ')

        doc = self.nlp(text)
        labels = [ent.label_ for ent in doc.ents]

        self.d_spacy = {ent.text:normalize_label(ent.label_) for ent in doc.ents}

        if self.iteration_nb == 0 and labels == ['LOC'] or (len(labels) > 1 and labels[0] == 'LOC'):
            self.d_warn = {**self.d_warn,**{'NO ENTITY FOUND BY SPACY ON FIRST RUN': 'WARN07'}}

        tracker = 0

        """
        # Be sure content not found by Spacy gets buffered
        if self.iteration_nb == 0:
            self.text_buffer = self.text_remaining
            for entity in doc.ents:
                    self.text_buffer = self.text_buffer.replace(entity.text, '')
            self.text_buffer = self.text_buffer.strip()"""

        for entity in doc.ents:

            force_label_loc = False

            start, end = entity.start_char, entity.end_char
            self.checking_main_entity = False # Tracer to differentiate handling of main entity from rest

            entity_text = entity.text

            # If not first round (text_buffer2 not empty), takes content from previous findings

            if self.text_buffer2 in entity_text:
                entity_text = entity_text.replace(self.text_buffer2, '')
                entity_text = entity_text.strip()
            elif entity_text in self.text_buffer2:
                entity_text = self.text_buffer2.replace(entity_text, '')
                entity_text = entity_text.strip()

            # NER entities -----------

            if entity.label_ == 'PERSON' or entity.label_ == 'ORG':

                # If option set, checks that two following entities are adjacent in the text
                if self.ADJACENT_ENTITIES:
                    adjacent_cond = tracker==0 or tracker <= start <= tracker+self.ADJACENT_ENTITIES_TOL

                # If not option set, ignore adjacent condition (i.e. always true)
                else:
                    adjacent_cond = True

                if adjacent_cond: # Checks if entities are adjacent

                    if self.check_payment_standard:

                        # Checks against the real payment structure (i.e. split by line)
                        if not self.ignore_entity_plausibility_check_structure:
                            entity_text = self.entity_plausibility_check_structure(entity_text)

                        if not self.has_plausible_main_entity:
                            self.d_warn = {**self.d_warn, **{'NO MAIN ENTITY FOUND': 'WARN02'}}

                        if entity_text is None:
                            continue

                        # Checks that libpostal doesn't find any non tolerated tags in the entity
                        check_no_address = self.entity_plausibility_check_postal(entity_text,tags_tolerated=self.POSTAL_ENTITY_TAGS_TOLERATED_IN_SPACY)

                        # Assigns content as entity
                        if check_no_address:
                            self.text_ner += ' '+entity_text
                            self.text_ner = self.text_ner.strip()
                            self.d_ner[entity_text] = normalize_label(entity.label_)
                            self.text_rest = self.text_rest.replace(entity_text,'').strip()

                        # If address suspected and main entity found, passes to LOC
                        if not check_no_address and not self.checking_main_entity :
                            force_label_loc = True

                        # If address suspected and main entity found, no pass to LOC
                        elif not check_no_address and self.checking_main_entity and self.has_plausible_main_entity:
                            self.d_warn = {**self.d_warn, **{'MAIN ENTITY MIGHT CONTAIN ADDRESS': 'WARN03'}}
                            self.d_ner[entity_text] = normalize_label(entity.label_)


                # If no adjacent entities: passes as LOC
                else:
                    force_label_loc = True
                    pass

                tracker = end

            # LOC entities -----------

            if entity.label_ == 'LOC' or force_label_loc:

                if self.iteration_nb == 0:
                    self.d_loc_spacy[entity_text] = 'LOC'
                    #self.d_addr = {**self.d_addr, **dict(pypostal_tc(self.text_addr, parse_address(entity_text)))}
                    self.text_addr += ' '+ entity_text
                    self.text_addr = self.text_addr.strip()
                else:
                    #self.d_addr = {**self.d_addr, **dict(pypostal_tc(self.text_addr, parse_address(entity_text)))}
                    self.d_rest[entity_text] = 'LOC'
                    #pass

            else:
                pass

        # To get one single label (but all labels still in d_ner)

        PER = any([True for e in doc.ents if e.label_ == 'PERSON'])
        ORG = any([True for e in doc.ents if e.label_ == 'ORG'])

        if PER and not ORG:
            self.spacy_ent = 'PER'
        elif not PER and ORG:
            self.spacy_ent = 'ORG'
        elif PER and ORG:
            self.spacy_ent = 'PER_ORG'
        else:
            self.spacy_ent = 'OTHER'

        return self

    def extract_addr(self,text=None):

        if text is None:
            pass
            #self.text_addr += ' '+self.text_country_code
        else:
            self.text_addr = text

        # Removing secondary splitters
        for s in self.LOC_SPLITTER_CANDIDATES:
            self.text_addr = self.text_addr.replace(s, ' ')

        # Parsing address fields using libpostal

        self.d_addr = {**self.d_addr,**dict(pypostal_tc(self.text_addr,parse_address(self.text_addr)))}

        if self.iteration_nb > 0:
            for k,v in self.d_addr.items():
                if v != 'country_code':
                    self.text_buffer = self.text_buffer.replace(k,'')
                    self.text_buffer = self.text_buffer.strip()

        if self.iteration_nb == 0 and self.d_addr == {}:
            self.d_warn = {**self.d_warn, **{'NO MAIN ADDRESS FOUND': 'WARN10'}}

        # If first round, one wants a minimum nb of fields to retry on Spacy below, otherwise returns
        if self.check_payment_standard and self.iteration_nb == 0:
            self.address_plausibility_check()
            if not self.has_plausible_address:
                return self

        # Re-passing some dupplicated tags to ner and find in case no yet main entity found
        if self.check_payment_standard:

            if not self.has_plausible_main_entity or self.has_plausible_main_entity:

                duppl_tags = find_duplicates(self.d_addr.values())

                # Higher position dupplicated tags must be NER
                to_investigate_tags = [tag for tag in duppl_tags if tag in self.POSTAL_ENTITY_DUPLICATED_TO_TREAT_AS_ENT]

                if len(to_investigate_tags) > 0:
                    for k in get_min_pos_text(self.d_addr, to_investigate_tags, self.text_ls_remaining):
                        #self.extract_ner(k)
                        self.d_ner[k] = 'PER_ORG'
                        del self.d_addr[k]

                # No city or country on first line
                to_investigate_tags = [tag for tag in self.POSTAL_ENTITY_FIRST_LINE_TO_TREAT_AS_ENT]
                if len(to_investigate_tags) > 0:
                    d_addr_ = self.d_addr.copy()
                    for k,v in d_addr_.items():
                        if v in to_investigate_tags:
                            pos = get_pos(k, self.text_ls_remaining, option='naive', selection='min')
                            if pos is not None and pos == 0: #and len(pos) == 1 and pos[0] == 0:
                                #self.d_ner[k] = 'PER_ORG'
                                self.extract_ner(k)
                                del self.d_addr[k]

                        else:
                            pass


                # Other tags back to NER check
                to_investigate_tags = [tag for tag in duppl_tags if tag in self.POSTAL_ENTITY_DUPLICATED_TAGS_TO_RETRY_ON_SPACY and tag not in self.POSTAL_ENTITY_DUPLICATED_TO_TREAT_AS_ENT]
                if len(to_investigate_tags) > 0:

                    for k, v in self.d_addr.items():
                        if v in to_investigate_tags:
                            #self.extract_ner(k)
                            self.text_buffer += ' '+k
                            self.text_buffer = self.text_buffer.strip()

                    d_ner_ = self.d_ner.copy()
                    for k,v in self.d_ner.items():
                        if k not in d_ner_ and k in self.d_addr:
                                #if k not in self.d_ner:
                            del self.d_addr[k]
                            entity_text = k
                            self.text_rest = self.text_rest.replace(entity_text, '').strip()

            stop = False
            for tag in self.POSTAL_ENTITY_TAGS_TO_RETRY_ON_SPACY:
                if tag not in duppl_tags and tag in self.d_addr.values() and not stop:
                    d_ = self.d_addr.copy()
                    for k, v in d_.items():
                        if v == tag:

                            # First pass (on text_addr): adds findings to buffer
                            #if self.iteration_nb == 0 and len(k.split()) >= self.POSTAL_ENTITY_MIN_LENGTH_TO_RETRY_ON_SPACY:
                            #if len(k.split()) >= self.POSTAL_ENTITY_MIN_LENGTH_TO_RETRY_ON_SPACY:
                            if len(re.split("[ -.]",k)) >= self.POSTAL_ENTITY_MIN_LENGTH_TO_RETRY_ON_SPACY or v == 'house':
                                self.text_buffer += ' '+k
                                self.text_buffer = self.text_buffer.strip()
                                self.text_rest = self.text_rest.replace(self.text_buffer,'')
                                self.d_addr = {key: val for key, val in self.d_addr.items() if val != tag}

                            # Second pass (on text_buffer): remove findings form buffer
                            else:
                                pass
                                #self.text_buffer = self.text_buffer.replace(k,'')
                                #self.text_buffer = self.text_buffer.strip()


                            self.text_buffer = self.text_buffer.strip()
                            self.d_warn = {**self.d_warn,**{'ENTITY MIGHT CONTAIN ADDRESS - TAG {}'.format(tag): 'WARN04'}}
                            stop = True # If first tag found: we stop
                            break

                else:
                    pass


            # To force some tags as NER if belonging to some ENT group identified in first run
            if self.iteration_nb > 0:
                to_investigate_tags = ['house']
                if len(to_investigate_tags) > 0:
                    d_addr_ = self.d_addr.copy()
                    for k,v in d_addr_.items():
                        if v in to_investigate_tags:
                            pos = get_pos(k, self.text_ls_remaining, option='naive', selection='min')
                            if self.iteration_nb > 0 and pos is not None and pos == 1:
                                for kk,vv in self.d_spacy.items():
                                    if k in kk and (vv == 'PER' or vv=='ORG'):
                                        self.d_ner[k] = 'PER_ORG'
                                        del self.d_addr[k]

                        else:
                            pass

            # Cleaning buffer from what stays in d_addr
            for k,v in self.d_addr.items():
                if v not in self.POSTAL_ENTITY_TAGS_TO_RETRY_ON_SPACY and v not in ['country_code']:
                    self.text_buffer = self.text_buffer.replace(k, '')



        return self   

    def detect_field_type(self):

        # Detects if text is 'ADDRESS_ENTITY' or 'FREE_TEXT'
        # This property can then be used in heuristics_tuning()

        self.field_type = recognizer.predict(self.text)

    def acronym_filter(self,filter_type = 'ORG'):

        # Checks if entity contains acronym

        # Acronym short lists
        # TODO: expand acronym list for companies/individuals

        if filter_type == 'ORG':           
            acr_ls = self.ORG_ACRONYMS
            ls = self.text_ls_raw # We want to capture uppercase acronyms like AG here

        elif filter_type == 'PER':
            acr_ls = self.PER_ACRONYMS
            ls = self.text_ls_remaining

        # Loops over entities

        k_to_replace = None

        #for t in ls:

            #k_to_replace_ls = find_best_lowercase_match(t,self.d_ner.keys())

        for k,v in self.d_res.items():

            k_to_replace_ls = [k]

            if len(k_to_replace_ls) > 0:
                k_to_replace = k_to_replace_ls[0]
            else:
                k_to_replace = None
                pass

            has_acr_ls = []

            #for w in t.split():
            for w in k.split():

                has_acr = any([True for acr in acr_ls if acr == remove_last_dot(w)])
                has_acr_ls.append(has_acr)

            if any(has_acr_ls):

                if k_to_replace is None:
                    self.d_warn = {**self.d_warn, **{'ENTITY ACRONYM FOUND IN LOC FIELD': 'WARN05'}}

                if filter_type == 'ORG':
                    self.has_acronym_org = True
                elif filter_type == 'PER':
                    self.has_acronym_per = True

                if k_to_replace is not None and k_to_replace in self.d_ner:
                    if self.d_ner[k_to_replace] == 'PER_acr' or self.d_ner[k_to_replace] == 'ORG_acr':
                        self.d_ner[k_to_replace] = 'PER_ORG_acr'
                    else:
                        self.d_ner[k_to_replace] = filter_type + '_acr'
                elif k_to_replace is not None and k_to_replace in self.d_rest:
                    if self.d_rest[k_to_replace] == 'PER_acr' or self.d_rest[k_to_replace] == 'ORG_acr':
                        self.d_rest[k_to_replace] = 'PER_ORG_acr'
                    else:
                        self.d_rest[k_to_replace] = filter_type + '_acr'

                else:
                    #self.d_ner[t] = filter_type + '_acr'
                    pass
                        
    def first_name_filter(self):

        # Checks if entity contains first name
                  
        for k,v in self.d_ner.items():

            is_first_name_ls = []

            if v == 'ORG' or v == 'PER':

                for w in re.findall(r"[\w']+", k):  # Different splitters to split composed names like 'Jean-Pierre'

                    w_no_accent = unidecode.unidecode(w)         
                    is_first_name = (w.lower() in d_first_names or w_no_accent in d_first_names)
                    is_first_name_long_enough = (is_first_name and len(w) >= self.FIRST_NAME_MIN_LEN)
                    is_first_name_ls.append(is_first_name_long_enough)
                    
            if any(is_first_name_ls): # and len(k.split()) <= 2:

                self.has_first_name = True

                if self.check_first_name and v == 'ORG':
                    self.d_ner[k] = 'PER_ORG'

                elif self.check_first_name and v == 'PER':
                    self.d_ner[k] = 'PER'
                    
        return self  
    
    def regex_filter(self):
        
        # Warn if entity or unexpected location contains numbers

        numeric_regex = re.compile('[0-9]')

        d_ = self.d_ner.copy()
        has_numeric_regex_ls = []
        for k, v in d_.items():
            if 'PER' in v or 'ORG' in v:
                for w in k.split():
                    check = numeric_regex.search(w) is not None
                    has_numeric_regex_ls.append(check)
                if any(has_numeric_regex_ls):
                    self.has_regex = True
                    if self.check_regex:
                        #del self.d_ner[k]
                        self.d_warn = {**self.d_warn, **{'NUMERIC FOUND IN MAIN ENTITY OR IN UNEXPECTED LOCATIONS': 'WARN06'}}

        for k,v in self.d_addr.items():
            if v != 'house_number' and v!= 'postcode':
                for w in k.split():
                    check = numeric_regex.search(w) is not None
                    has_numeric_regex_ls.append(check)
                if any(has_numeric_regex_ls):
                    self.has_regex = True
                    if self.check_regex:
                        #del self.d_ner[k]
                        self.d_warn = {**self.d_warn, **{'NUMERIC FOUND IN MAIN ENTITY OR IN UNEXPECTED LOCATIONS': 'WARN06'}}


        # Symbol pattern

        symbol_regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

        d_ = self.d_ner.copy()
        has_symbol_regex_ls = []
        for k,v in d_.items():
            if v == 'PER':
                for w in k.split():
                    check = symbol_regex.search(w) is not None
                    has_symbol_regex_ls.append(check)
                if any(has_symbol_regex_ls):
                    self.has_regex = True
                    if self.check_regex:
                        self.d_ner[k] = 'ORG'

        return self 
        
    def cleaning_postprocessing(self):

        # Find dupplicates text

        duppl_tokens = [k for k in self.d_res.keys() if k in self.d_addr.keys()]
        tags = []
        for t in duppl_tokens:
            if t in self.d_ner and t in self.d_addr:
                self.d_ner[t] = 'LOC_' + self.d_ner[t]
                del self.d_addr[t]
            else:
                pass

        # Removing stop words in the begin/end of entities

        self.d_ner = clean_stopwords(self.d_ner, stopwords=self.STOPWORDS)

        # Removing empty entity items and stripping

        self.d_ner = {k.strip():v for k,v in self.d_ner.items() if v!= '' or v=="'"}

        return self

    def tfidf_filter(self):

        # Loops over entities

        #TODO Add bigram search

        #import pdb;pdb.set_trace()

        for k, v in self.d_ner.items():

            pred = tfidf.predict_entity(k.lower(), option='any_company2',
                                        tfidf_company_thres=self.TFIDF_COMPANY_THRES,
                                        tfidf_comparison_fact_org=self.TFIDF_COMPARISON_FACT_ORG,
                                        tfidf_comparison_fact_per=self.TFIDF_COMPARISON_FACT_PER,
                                        stopwords=self.STOPWORDS)
            if pred != self.d_ner[k]:
                self.has_tfidf_changed = True
                self.d_ner[k] = 'PER_ORG_tf_found'
            if pred == 'ND':
                self.has_tfidf_changed = True
                self.d_ner[k] =  v + '_tf_nd'
            else:
                pass

        return self

    def get_confidence_spacy(self):

        # Checks confidence level using spacy beam search (global confidence)
        
        with self.nlp.disable_pipes('ner'):
            doc = self.nlp(self.text)

        beams = self.nlp.entity.beam_parse([ doc ], beam_width = 16, beam_density = 0.0001)
        entity_scores = defaultdict(float)
        
        for beam in beams:
            for score, ents in self.nlp.entity.moves.get_beam_parses(beam):
                for start, end, label in ents:
                    entity_scores[(start, end, label)] += score
    
        low_conf = False
        
        if entity_scores == {}:
            low_conf = True

        # --------
        # Option 1 - Zero tolerance

        if self.confidence_spacy == 'high':
            try:
                key_min = min(entity_scores.keys(), key=(lambda k: entity_scores[k]))
                min_val = entity_scores[key_min]
            except:
                min_val = 0

            if min_val < 1 :
                low_conf = True

        # --------
        # Option 2 - Small tolerance for PER
        
        elif self.confidence_spacy == 'medium':   
            low_conf_item = False
            low_conf_ls = []
            for key in entity_scores:
                start, end, label = key
                if label == 'PERSON' and entity_scores[key] < self.SPACY_CONFIDENCE_PER:
                    low_conf_item = True
                elif label == 'ORG' and entity_scores[key] < self.SPACY_CONFIDENCE_ORG:
                    low_conf_item = True
                low_conf_ls.append(low_conf_item)
            low_conf = any(low_conf_ls)
        
        self.entity_scores = entity_scores 

        return low_conf

    def spacy_confidence_filter(self):

        # Removing low confidence decisions

        low_conf = self.get_confidence_spacy()

        if low_conf:

            self.has_low_spacy_confidence = True
            self.d_ner = {k: 'PER_ORG_beam_conf' for k,v in self.d_ner.items()}

    def heuristics_tuning(self):

        # Applies additional heuristics
            
        if self.field_type == 'ENTITY_ADDRESS':
                               
            # No entity was found
            key_org_new = self.text_ner.strip()
            cond0 = len(self.d_ner) == 0
            if cond0:
                self.has_heuristics_tuning = True
                if self.check_heuristics_tuning:
                    self.d_ner[key_org_new]  = 'ORG'
                    self.d_res[key_org_new]  = 'ORG'
                
                return self
            
            # Some ORG was found, but partial
            cond1 = 'PER' not in list(self.d_ner.values())

            if cond1:
                self.has_heuristics_tuning = True
                if self.check_heuristics_tuning:
                    self.d_ner = {}
                    self.d_ner[key_org_new]  = 'ORG'

                return self
    
        elif self.field_type == 'FREE_TEXT':

            """
            # If only one word in entity, sets PER to be safe
            key_org_new = self.text_ner.strip()
            cond0 = len(key_org_new.split()) == 1
            if cond0:
                self.d_ner[key_org_new]  = 'PER'
            """

            pass
            
            return self

    def entity_plausibility_check_structure(self,text):

        text_pred = text
        text_pred_lower = text_pred.lower()

        res = []

        if len(self.text_ls_remaining) > 0:

            for ind,text_real in enumerate(self.text_ls_remaining):

                cond = False
                text_real_lower = text_real.lower()

                # Other trial: if self.ENTITY_PLAUSIBILITY_THRESHOLD <= similar(text_pred_lower, text_real_lower) < 1:

                matches = get_matches(text_real_lower, text_pred_lower)[0:-1] # Removes last match element (zero-length)
                if len(matches) == 0:
                    continue

                #For main entity, we want a match in the beginning of the line
                if not self.has_plausible_main_entity and ind < self.MAIN_ENTITY_MAIN_IND:
                    self.checking_main_entity = True
                    first_match = matches[0]
                    cond = min(m.size for m in matches)  >= self.MATCH_SIZE and first_match.a == 0
                    if cond:
                        self.has_plausible_main_entity = True
                        ls_ = []
                        for m in matches:
                            ls_.append(text_real[m.a:m.a+m.size])
                        text_common = ' '.join(ls_)
                        if len(text_common) < len(text_pred_lower):
                            self.text_buffer += '' + text_pred.replace(text_common,'')
                            self.text_buffer = self.text_buffer.strip()
                            res = text_common
                        elif len(text_common) >= len(text_pred_lower):
                            self.text_buffer2 += '' + text_real.replace(text_common, '')
                            self.text_buffer2 = self.text_buffer2.strip()
                            res = text_real

                        return res
                    else:
                        pass

                #For others, we takes matches anywhere
                else:
                    self.checking_main_entity = False
                    cond = min(m.size for m in matches) >= self.MATCH_SIZE
                    if cond:
                        ls_ = []
                        for m in matches:
                            ls_.append(text_real[m.a:m.a + m.size])
                        text_common = ' '.join(ls_)
                        if len(text_common) < len(text_pred_lower):
                            self.text_buffer += '' + text_pred.replace(text_common,'')
                            self.text_buffer = self.text_buffer.strip()
                            res = text_common
                        elif len(text_common) >= len(text_pred_lower):
                            res = text_real
                        return res
                    else:
                        pass
            return None
        
        else:
            return None

    def entity_plausibility_check_postal(self,text,tags_tolerated=['house']):

        ls_ = parse_address(text)
        if len(ls_) > 0:
            checks = [True if t[1] in tags_tolerated else False for t in ls_]
            return all(checks)
        else:
            return True

    def address_plausibility_check(self):

        # Enough address fields
        cond1 = len(self.d_addr.values()) >= self.NB_MIN_ADDRESS_FIELDS
        cond2 = any([True if v in self.d_addr.values() else False for v in self.MINIMUM_REQUIRED_FIELD_LIBPOSTAL])
        cond3 = False
        if 'state' in self.d_addr.values():
            if 'country' in self.d_addr.values():
                cond3 = True
        else:
            cond3 = True

        # Checking if specific tags split over many elements
        cond4 = True
        if 'city' in self.d_addr.values():
            for k,v in self.d_addr.items():
                if v == 'city':
                    text = k
                    ls = []
                    for w in text.split():
                        pos = get_pos(w, self.text_ls_remaining, option='naive', selection='all')
                        ls.append(pos)
                    if len(ls) > 1:
                        cond4 = False

        # Doesn't toleate 2 house numbers

        cond5=True
        duppl_tags = find_duplicates(self.d_addr.values())
        if 'house_number' in duppl_tags:
            cond5=False

        # Forbids not sufficient sequences

        cond6=True
        check = []

        for s in self.NOT_SUFFICIENT_TAGS:
            if set(self.d_addr.values()) == set(s):
                check.append(True)
        if any(check):
            cond6=False

        #Summary
        if cond1 and cond2 and cond3 and cond4 and cond5 and cond6:
        #if cond1 and cond2 and cond3 and cond4:
            self.has_plausible_address = True
        else:
            self.d_warn = {**self.d_warn,
                           **{'ADDRESS FIELDS DO NOT MEET REQUIREMENTS': 'WARN09'}}

        """
        # Removes dupplicates using ordering
        duppl_tags = find_duplicates(self.d_ner.items())
        to_investigate_tags = [tag for tag in duppl_tags if
                                   tag in self.POSTAL_ENTITY_DUPLICATED_TO_TREAT_AS_ENT]

        # Check in which position does which dupplicated city or country appear
        d_ = {}
        for tag in to_investigate_tags:
            for k,v in self.d_ner.items():
                d_[k] = []
                if tag==v:
                    pos_ls = [e for e,s in enumerate(self.text_ls) if tag in s]
                    if len(pos_ls) == 1:
                        pass
                    else:
                        pass

        # Cleaning according to findings
        #TODO

        #if self.d_loc_spacy == {}:
        #    self.has_plausible_address = False
        """

    def order_plausibility_check(self):

        res = []
        df_check = get_text_tag_pos_df(d=self.d_res, ls=self.text_ls_remaining)
        df_check['tag'] = df_check['tag'].apply(categorize_ent)

        for t in self.TOLERATED_SEQ:

            check = check_order(t=t, df=df_check)
            if all(True if i in df_check['tag'].tolist() else False for i in t):
                if False in check:
                    res.append(False)
            else:
                res.append(True)

        if not all(res):
            self.d_warn = {**self.d_warn,
                           **{'ORDER OF TAGS DO NOT MEET REQUIREMENTS': 'WARN11'}}

    def extract_rest(self):

        self.text_rest = self.text_remaining
        #import pdb;pdb.set_trace()
        for k,v in self.d_res2.items():
            if k in self.text_rest:
                self.text_rest = self.text_rest.replace(k,'')

        self.text_rest = self.text_rest.strip()
        if len(self.text_rest) != 0:
            self.d_warn = {**self.d_warn, **{'REST STRING NOT PARSED OF LENGTH {}'.format(len(self.text_rest)): 'WARN08'}}

        # Creates a dictionary of tagged fields of rest (i.e. not entity and not address)

        if self.create_nlp_tags_rest_text and ENABLE_RECOGNIZER:
            tuple_ls = get_nlp_tuple_seq(self.text_rest,lib=self.pos_library)
            self.d_rest = {**self.d_rest,**dict(tuple_ls)}
        else:
            pass
                
        return self

    def create_nlp_indicators(self):

        # Tags full content using spacy and corenlp for possible downstream processing

        s1 = get_nlp_tuple_seq(self.text, lib='spacy')
        s2 = get_nlp_tuple_seq(self.text, lib='corenlp')

        self.nlp_tags = combine_seq2(s1, s2)

        for w in self.text_ner.split():
            for t in self.nlp_tags:
                if w.lower() == t[0]:
                    self.nlp_tags_ner.append(t)  # Text and tag
                    self.nlp_tags_ner.append(t[1])  # Tag only

        return self

class ExtractorSwiftPaymentWrapperClass(object):

    def __init__(self,text,splitter=None,remove_non_plausible=True):

        self.text = text
        self.splitter = splitter
        self.payment_processing()
        self.parse_parts()

        self.is_plausible = True
        if remove_non_plausible:
            if not self.is_plausible:
                self.d_res = self.d_ner = self.d_loc = {'MESSAGE':'STRUCTURE NON PLAUSIBLE'}

    def payment_processing(self):

        # Removes splitter from text

        self.text_raw = self.text
        self.test_ls_raw = self.text_raw.split(self.splitter)
        self.test_ls_raw = [e for e in self.test_ls_raw if e != '']
        self.text = self.text_raw.replace(self.splitter, ' ')

        return self

    def parse_parts(self):

        #import pdb;pdb.set_trace()

        self.d_res = {}
        self.d_ner = {}
        self.d_loc = {}

        for i,txt in enumerate(self.test_ls_raw):

            e = ExtractorClass(txt, check_tfidf = True, check_spacy_confidence=False,
                       check_heuristics_tuning=False)
            d_res_ = e.d_res
            d_ner_ = e.d_ner
            d_loc_ = e.d_loc_spacy

            # Checks plausiblity (one entity per line, PER or ORG on first line)
            if len(d_ner_.keys()) > 1 or len(d_loc_.keys()) > 1:
                self.is_plausible = False
            if i == 0:
                for v in d_res_.values():
                    if 'PER' in v or 'ORG' in v: # Also plausible for PER_ORG_x flags
                        self.is_plausible = True
                    else:
                        self.is_plausible = False

            self.d_res = {**self.d_res, **d_res_}
            self.d_ner = {**self.d_ner, **d_ner_}
            self.d_loc = {**self.d_loc, **d_loc_}
            print("Parsed fields (d_res2)",self.d_ner2)

        return self

if __name__ == '__main__':

    HOME_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, HOME_DIR)
