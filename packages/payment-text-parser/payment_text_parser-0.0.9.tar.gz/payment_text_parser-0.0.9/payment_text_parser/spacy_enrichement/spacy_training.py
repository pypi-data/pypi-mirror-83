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

from __future__ import unicode_literals, print_function

import os
import sys

import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding
from payment_text_parser.data_generator.data_generator import GeneratorClass

import logging
logging.basicConfig(filename="spacy_enrichment.log",
                    filemode='a+',
                    level=logging.INFO,format="%(asctime)s %(levelname)-8s %(message)s")

from spacy.util import decaying

# Parameters
VERSION='0.0.72'
SAMPLE_SIZE = 100000
FIELD_TYPE_RATIO = round(1,2) #We put only address to emphasize on use case
#FIELD_TYPE_RATIO = round(0,2) #We put only free text to emphasize on use case
FIELD_TYPES = {'ENTITY_ADDRESS':FIELD_TYPE_RATIO,'FREE_TEXT':round(1-FIELD_TYPE_RATIO,2)}
FIELD_PATTERN_FLAVOR = 'location_entity_flavor'
#FIELD_PATTERN_FLAVOR = 'per_org_flavor'
#DROP = 0.1
DROP = 'drop_decay'
N_ITER = 20
MAX_BATCH_SIZE = 16

if FIELD_PATTERN_FLAVOR == 'location_entity_flavor':
    FIELD_PATTERN_FLAVOR_SHORT = 'LOC-ENT'
elif FIELD_PATTERN_FLAVOR == 'per_org_flavor':
    FIELD_PATTERN_FLAVOR_SHORT = 'PER-ORG'

MODEL_NAME = '{}_{}_{}_{}'.format(FIELD_PATTERN_FLAVOR_SHORT,str(SAMPLE_SIZE),FIELD_TYPE_RATIO,VERSION)

# Logging
logging.info("Model name : "+MODEL_NAME)
logging.info("--------------------------------")
logging.info("Sample size : "+str(SAMPLE_SIZE))
logging.info("Field types: "+str(FIELD_TYPES))
logging.info("Field pattern flavor: "+FIELD_PATTERN_FLAVOR)
logging.info("Drop: "+str(DROP))
logging.info("Nb iterations: "+str(N_ITER))
logging.info("Max batch size: "+str(MAX_BATCH_SIZE))
logging.info("Model training...")

# Examples - Training scraping
#
#TRAIN_DATA = [
#    ("Mietzins", {"tags": ["NN"]}),
#    ("Der Mietzins ist noch gestiegen.", {"tags": ["ART", "NN", "VAFIN", "ADV", "VVPP", "$."]})
#    #("Kurt", {"tags": ["NE"]})
#]

#TRAIN_DATA = [
#    ("Rechnung Kurt Arbin", {"entities": [(9, 22, "PER")]}),
#    ("I like London and Berlin.", {"entities": [(7, 13, "LOC"), (18, 24, "LOC")]})
#]

g = GeneratorClass(SAMPLE_SIZE,field_pattern_flavor=FIELD_PATTERN_FLAVOR,field_types=FIELD_TYPES)
TRAIN_DATA = g.train_data

#Get data
g.save_data(option = 'train',filename='train_data_web_address_{}.csv'.format(MODEL_NAME))
g.save_data(option = 'test',filename='test_data_web_address_{}.csv'.format(MODEL_NAME))

OUTPUT_DIR = "../models/spacy_models/custom_de_core_news_sm_{}/".format(MODEL_NAME)

@plac.annotations(
    lang=("ISO Code of language to use", "option", "l", str),
    n_iter=("Number of training iterations", "option", "n", int),
)
def main(lang="en",
         output_dir=OUTPUT_DIR,n_iter=N_ITER):
    """Create a new model, set up the pipeline and train the tagger. In order to
    train the tagger with a custom tag map, we're creating a new Language
    instance with a custom vocab.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    new_model = True
    
    if new_model:
        nlp = spacy.blank(lang)
        #nlp = spacy.blank()
    else:
        nlp = spacy.load('de_core_news_sm')
        
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    else:
        ner = nlp.get_pipe("ner")
        
    # add labels

    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            try:
                ner.add_label(ent[2])
            except:
                import pdb;pdb.set_trace()

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    
    with nlp.disable_pipes(*other_pipes):

        optimizer = nlp.begin_training()
        for i in range(N_ITER):
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            #batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            batches = minibatch(TRAIN_DATA, size=compounding(1, MAX_BATCH_SIZE, 1.001))
            dropout = decaying(0.6, 0.2, 1e-4)
            for batch in batches:
                texts, annotations = zip(*batch)
                try:
                    drop = next(dropout)
                    nlp.update(texts, annotations, sgd=optimizer, losses=losses,drop=drop)
                except:
                    print("Check if scraping format ok (missing values)")
                    
            print("Losses", losses)

    logging.info("Final losses : "+str(losses))

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)

    logging.info("Model trained and saved in : "+str(output_dir))
    logging.info("******************************************")

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    plac.call(main)