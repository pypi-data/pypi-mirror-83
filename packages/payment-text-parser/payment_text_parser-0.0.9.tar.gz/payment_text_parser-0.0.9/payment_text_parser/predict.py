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

from payment_text_parser.entity_extractor.entity_extractor import ExtractorClass, ExtractorSwiftPaymentWrapperClass
from payment_text_parser.data_generator.data_generator import TfIdf

def get_pred_ptparser_wrapper():
    from flask import Flask, request
    json_data = request.get_json()
    text = json_data['text']

    #import pdb;pdb.set_trace()
    ew = ExtractorSwiftPaymentWrapperClass(text,splitter='@')

    d_res = {**ew.d_ner,**ew.d_loc}

    return d_res

def get_pred_ptparser():
    from flask import Flask, request
    json_data = request.get_json()
    text = json_data['text']

    print(text)
    #print(request.remote_addr)

    e = ExtractorClass(text, check_payment_standard= True, check_tfidf = True, check_spacy_confidence=False,
                       check_heuristics_tuning=False, create_nlp_tags_rest_text=True,
                       create_nlp_tags_full_text=False)

    #return {k:v for k,v in e.d_res.items() if v != 'WARN04'} # For demo website
    #return e.d_res # Complete libpostal output
    return e.d_res2 # Simplified output

def get_pred_ptparser_free_text():
    from flask import Flask, request
    json_data = request.get_json()
    text = json_data['text']

    print(text)

    e = ExtractorClass(text, language='XX', field_type='FREE_TEXT',
                       pos_library='corenlp', confidence_spacy='high', check_true_case=True, check_language=False,
                       check_field_type=False, check_payment_standard=False, check_tfidf=False, check_acronyms_per=True,
                       check_acronyms_org=True, check_first_name=False,
                       check_regex=True, check_spacy_confidence=True, check_heuristics_tuning=True,
                       create_parsed_address=True, create_nlp_tags_rest_text=True, create_nlp_tags_full_text=False,
                       custom_tech_words=['MIST'])
    #import pdb;pdb.set_trace()
    return e.d_spacy

def get_pred_tfidf():
    from flask import Flask, request
    json_data = request.get_json()
    text = json_data['text']

    tfidf = tfidf = TfIdf()
    pred = tfidf.predict_entity(text,option='any_company')
    d_res = {}
    d_res[text] = pred
    return d_res