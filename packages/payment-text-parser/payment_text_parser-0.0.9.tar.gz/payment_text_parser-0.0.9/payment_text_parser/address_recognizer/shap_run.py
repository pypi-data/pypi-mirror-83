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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from payment_text_parser.address_recognizer import Recognizer

import shap
shap.initjs()

#import matplotlib.pyplot as plt

# Ref

#https://slundberg.github.io/shap/notebooks/deep_explainer/Keras%20LSTM%20for%20IMDB%20Sentiment%20Classification.html

# Load model

r1 = Recognizer('concat',sample_size = 10)
#r1.make_model()
r1.load_model()

model = r1.model
x_train = r1.x_train
x_test = r1.x_test
df = r1.df
df_feat = df.drop(['y'],axis=1)
feature_names=df_feat.columns

print("Model and scraping loaded.")

# E2E

explainer = shap.DeepExplainer(model, x_train[:100])

# DeepExplainer

# select a set of background examples to take an expectation over
#background = x_train[np.random.choice(x_train.shape[0], 10, replace=False)]

"""
# explain predictions of the model on four images
e = shap.DeepExplainer(model, background)
shap_values = e.shap_values(x_test[1:5])"""

# Use Kernel SHAP to explain test set predictions

explainer = shap.KernelExplainer(model.predict_proba, x_train, link="logit")
shap_values = explainer.shap_values(x_test) #, nsamples=10)

# Plot the SHAP values for the Setosa output of the first instance
plt.savefig('books_read.png')
shap.force_plot(explainer.expected_value[0], shap_values[0][0,:], x_test[0,:],
                link="logit",feature_names=feature_names,
                matplotlib=False)    

# Visualize the training set predictions

#shap.force_plot(explainer.expected_value, shap_values[0], x_train)
a = shap.force_plot(explainer.expected_value, shap_values[0], x_train)

#from IPython.display import display
#a = display(a)

html = a.data
with open('html_file.html', 'w') as f:
    f.write(html)

# Dependance plot

#shap.dependence_plot("RM", shap_values, x_train)

# summarize the effects of all the features
shap.summary_plot(shap_values, x_train,feature_names=feature_names)

# shap.force_plot(explainer.expected_value[0], shap_values[0][0,:], x_test[0,:], link="logit",show=False)

# shap.force_plot(explainer.expected_value, shap_values[0,:], X.iloc[0,:],show=False)
# plt.savefig('scratch.png')
