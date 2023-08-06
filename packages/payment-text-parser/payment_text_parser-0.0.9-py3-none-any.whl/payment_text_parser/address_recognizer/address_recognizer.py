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
MODEL_DIR = os.path.join(HOME_DIR,'models/keras_models')

import pandas as pd
import numpy as np
import time
import pickle

from payment_text_parser.address_recognizer import address_recognizer_utils as utils
#from address_recognizer.recognizer_utils import get_concatenated_tag_text,get_combined_tag_text,get_combined_tag_length

from keras.preprocessing.text import Tokenizer	
from keras.models import Sequential
from keras.layers import Activation, Dense, Dropout
from keras.models import model_from_json

from sklearn.preprocessing import LabelBinarizer

from payment_text_parser.data_generator.data_generator import GeneratorClass

class Recognizer(object):
    
    def __init__(self,method='concat',sample_size = 100):
        
        # Model type
        
        self.method = method
        
        # Hyperparameters
        self.batch_size = 20
        self.train_ratio = 0.7
        
        # Filenames
        self.model_name = os.path.join(MODEL_DIR,'model_'+self.method)
        
        # Generate scraping
        print("Generate scraping..")
        self.SAMPLE_SIZE = sample_size
        g = GeneratorClass(n_sample=self.SAMPLE_SIZE,train_test = {'TRAIN':1,'TEST':0})
        self.df = g.get_format_data(option='train')
        #self.df = self.df[0:10]
        self.ref_feature_list = None
        
        self.preproc()
        
        # Pre-processing
    def preproc(self):
        if self.method == 'token_length':
            self.preproc2()
        else:
            self.preproc1()
            
        print("-------------------")
        return self
    
    def predict(self,text):
              
        self.df = pd.DataFrame([text],columns=['input'])
        self.tag_extraction()
        self.tokenize()
        self.enrichment()
        self.feature_alignment()
        self.make_data_frame()
        ynew = self.model.predict_classes(self.x,verbose = 0)
        
        label = self.encoder.inverse_transform(ynew)[0]
        
        return label
        
    ## Pipeline functions
    
    def preproc1(self):
        
        print("Feature extraction..")
        self.tag_extraction()
        print("Tokenizer..")
        self.tokenize()
        print("Enrichment..")
        self.enrichment()
        self.labels()
        self.make_data_frame()
        
        print("Process finished, raw scraping and features generated.")
        
        return self
    
    def preproc2(self):
        
        print("Feature extraction..")
        self.token_length_extraction()
        self.labels()
        print("Split train/test..")
        self.split()
        print("Process finished, raw scraping and features generated.")
        
        
    def make_model(self):
        
        start_time = time.time()
        
        print("Split train/test..")
        self.split()

        # Train
        print("Model training/evaluation..")
        self.train()
        self.evaluate()
        
        # Saving
        print("Model saving..")
        self.save()
        
        print("Process finished, model saved as :",self.model_name)
        
        elapsed_time = time.time() - start_time
        print("Time elapsed :",elapsed_time)
        
    
    def load_model(self):
        
        print("Model loading/evaluation..")
        self.load()
        self.feature_alignment()
        self.make_data_frame()
        self.split()
        self.evaluate()
        
        print("Process finished, model loaded.")
        
    
    ## Single functions

    # Features
    
    def token_length_extraction(self):
        
        ls = []
        for i,row in self.df.iterrows():

            d = utils.get_combined_tag_length(row['input'])
            ls.append(d)
        df = pd.DataFrame(ls)
        
        #import pdb;pdb.set_trace()
        self.feature_list = df.columns
        self.x = np.nan_to_num(df.values)
        
        return self
    
    def tag_extraction(self):
        
        # Method 1: unit tags concatenated
        if self.method == 'concat':
            self.df['tags']=self.df['input'].apply(utils.get_concatenated_tag_text)
        
        # Method 2: unit tags combined
        if self.method == 'combined':
            self.df['tags']= self.df['input'].apply(utils.get_combined_tag_text)
        
        return self
        
    # Tokenizer    
    def tokenize(self):
    
        # Features 
        df = self.df
        docs = df['tags'].tolist()
        
        # create the tokenizer
        t = Tokenizer(filters='')
        # fit the tokenizer on the documents
        t.fit_on_texts(docs)
        # summarize what was learned
        print(t.word_counts)
        print(t.document_count)
        print(t.word_index)
        print(t.word_docs)
        # integer encode documents
        encoded_docs = t.texts_to_matrix(docs, mode='count')
        #encoded_docs = t.texts_to_matrix(docs, mode='binary')
        self.x = encoded_docs
        self.feature_list = ['PAD']+[k for k,v in t.word_index.items()]
        # Cleaning required since '[' causes issue in dataframe
        self.feature_list  = [f.replace('[','') for f in self.feature_list]
                      
        
    #Enrichment
    def enrichment(self):
        
        ls = []
        for i,row in self.df.iterrows():
            d1 = utils.get_combined_tag_length(row['input'])
            d2 = utils.get_libpostal_tag_length(row['input'])
            d = {**d1, **d2}
            ls.append(d)
        df_enriched = pd.DataFrame(ls)
        
        #import pdb;pdb.set_trace()
        ind_cols = [i for i,c in enumerate(df_enriched.columns) if '_' in c and 'house' in c]
        df_enriched = df_enriched.iloc[:,ind_cols]
    
        x = np.nan_to_num(df_enriched.values)
        self.feature_list += list(df_enriched.columns)
        self.x = np.concatenate((self.x,x),axis=1)
        
        # Cleaning required since '[' causes issue in dataframe
        self.feature_list  = [f.replace('[','') for f in self.feature_list]
                    
    #Labels
    def labels(self):
            
        labels = list(self.df['field_type'])	
        encoder = LabelBinarizer()
        encoder.fit(labels)      
        self.y = encoder.transform(labels)
        
        # Useful    
        self.encoder = encoder
        self.text_labels = encoder.classes_
                
        return self
    
    # Single dataframe (raw input, features, output)    
    def make_data_frame(self):
        
        df_raw = self.df

        df_x = pd.DataFrame(self.x, columns = self.feature_list)
        df_y = pd.DataFrame(self.y,columns = ['y'])
        
        self.df = pd.concat([df_x,df_y],axis=1,sort=False)
        self.df_all = pd.concat([df_raw,df_x,df_y],axis=1,sort=False)
       
    # Split train/test
    def split(self):
    
        train_size = int(len(self.df) * self.train_ratio)
            
        self.df_train = self.df[:train_size]
        self.df_test = self.df[train_size:]
        
        self.x_train = self.x[:train_size]
        self.x_test = self.x[train_size:]
        self.y_train = self.y[:train_size]
        self.y_test = self.y[train_size:]
        
        return self
    
    # Train model    
    def train(self):

        #vocab_size = len(t.word_index)
        vocab_size = self.x.shape[1]
        #num_labels = len(encoder.classes_)
        
        
        # LSTM 1
               
        """
        input_length = self.x.shape[1]
        
        self.model = Sequential()
        self.model.add(Embedding(input_dim = 188, output_dim = 50, input_length = input_length))
        self.model.add(LSTM(output_dim=256, activation='sigmoid', inner_activation='hard_sigmoid', return_sequences=True))
        #self.model.add(Dropout(0.5))
        self.model.add(LSTM(output_dim=256, activation='sigmoid', inner_activation='hard_sigmoid'))
        #self.model.add(Dropout(0.5))
        self.model.add(Dense(1, activation='sigmoid'))
        """
        
        # Plain
                    
        self.model = Sequential()
        
        self.model.add(Dense(32, input_shape=(vocab_size,)))
        self.model.add(Activation('relu'))
        
        self.model.add(Dropout(0.1))
        self.model.add(Dense(16))
        self.model.add(Activation('relu'))
        #model.add(Dropout(0.3))
        self.model.add(Dense(1))
        self.model.add(Activation('sigmoid'))
                
        self.model.summary()      
        self.model_compile()        
        self.history = self.model.fit(
                self.x_train, self.y_train,
                batch_size=self.batch_size,
                epochs=40, #40 # 30
                verbose=1,
                validation_split=0.1)
        
        return self
    
    def model_compile(self):
         self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
         return self
    
    # Feature alignment
    def feature_alignment(self):
       
        if self.ref_feature_list is not None:
            # Using pandas to align current features to training features
            df_ref = pd.DataFrame(columns=self.ref_feature_list)
            df_aligned = pd.DataFrame(self.x,columns=self.feature_list)
            # Checking if new features must be drop since not in training
            feature_list_known = [f for f in self.feature_list if f in self.ref_feature_list]         
            df_aligned = df_aligned[feature_list_known]
            
            #import pdb;pdb.set_trace()
            df_aligned = df_aligned.align(df_ref,fill_value=0)[0]
            df_aligned = df_aligned[df_ref.columns]
            self.x = df_aligned.values
            self.feature_list = df_aligned.columns # = self.ref_feature_list

        else:
            print("No list of features found")
            
        return self
    
    # Evaluate     
    def evaluate(self):
        
        #import pdb;pdb.set_trace()
        
        #if self.x_test.shape[0]//self.batch_size != 0:
        #    self.batch_size = self.x_test.shape[0]
        
        # Generic
        score = self.model.evaluate(
                self.x_test, self.y_test,
                batch_size=self.batch_size, verbose=1)
        
        print('Test accuracy:', score[1])
        
        self.score = score
        
        # Custom
        y_pred = []
        
        for i in range(len(self.y_test)):
            prediction_prob = self.model.predict(np.array([self.x_test[i]]))
            if prediction_prob >= 0.5:
                prediction = 1
            else:
                prediction = 0
            y_pred.append(prediction)
            
            """
            if prediction != self.y_test[i]:
                print("One mismatch at index :",i)
                try:
                    print("Input :",self.df_test['input'].iloc[i])
                except:
                    import pdb;pdb.set_trace()
                print("------------------------")
            """
        
        self.y_pred = np.array(y_pred)
       
        return self
 
    # Save
    def save(self):
        
        # serialize model to JSON
        model_json = self.model.to_json()
        with open(self.model_name+".json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self.model.save_weights(self.model_name+".h5")
        print("Saved model to disk")
        # meta-scraping
        with open(self.model_name+'_metadata.pickle', 'wb') as f:
            pickle.dump(self.feature_list, f, protocol=pickle.HIGHEST_PROTOCOL)
      
    # Load
    def load(self)   :

        # load json and create model
        json_file = open(self.model_name+".json", 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        # load weights into new model
        self.model.load_weights(self.model_name+".h5")
        self.model_compile()
        
         # meta-scraping
        with open(self.model_name+'_metadata.pickle', 'rb') as f:
            self.ref_feature_list = pickle.load(f)
        
        
 # Run
 
def combine():

    r1 = Recognizer('concat',sample_size=1000)
    #r1.make_model()
    r1.load_model()
     
    r2 = Recognizer('token_length')
    #r2.make_model()
    r2.load_model()
    
    
    #r2 = Recognizer('combined')
    #r2.make_model()
    #r2.load_model()
    
    # Combine model
    
    if not all(r1.y_test == r2.y_test):
        print("Different y_test, change methods to use external y_test")
    else:
        y_test = r1.y_test.flatten()
        pass
    
    x = np.stack((r1.y_pred.flatten(),r2.y_pred.flatten()),axis=1)
    
    df_x = pd.DataFrame(x)
 
    df_y = pd.DataFrame(y_test)
    df = pd.concat([df_x,df_y],axis=1)
    df.columns = ['pred1','pred2','real']
        
    for i,row in df.iterrows():
        if (row[0] == row[1]) and (row[1] == row[2]):
            continue
        elif (row[0] == row[2]) and (row[1] != row[2]):
            print("For row :",i," only model 1 was right.")
        elif (row[0] != row[2]) and (row[1] == row[2]):
            print("For row :",i," only model 2 was right.")
        else:
            print("For row :",i,"no model was right.")

# Run fuc

def process():
    r1 = Recognizer('concat',sample_size=1000)
    #r1 = Recognizer('combined')
    #r1 = Recognizer('token_length')
    r1.make_model()
    #r1.load_model()
            
    #r3 = r1.copy()
    #r3.x = np.concatenate((r1.x,r2.x),axis=1)
    #r3.model_name = 'merge'
    #r3.make_model()
    
def plot():
    
    import matplotlib.pyplot as plt
    plt.style.use('ggplot')
    
    def plot_history(history):
        acc = history.history['acc']
        val_acc = history.history['val_acc']
        loss = history.history['loss']
        val_loss = history.history['val_loss']
        x = range(1, len(acc) + 1)
    
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.plot(x, acc, 'b', label='Training acc')
        plt.plot(x, val_acc, 'r', label='Validation acc')
        plt.title('Training and validation accuracy')
        plt.legend()
        plt.subplot(1, 2, 2)
        plt.plot(x, loss, 'b', label='Training loss')
        plt.plot(x, val_loss, 'r', label='Validation loss')
        plt.title('Training and validation loss')
        plt.legend()
        
# Process
   
#process()  
