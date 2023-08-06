# (C) Copyright 2020 Alpina Analytics GmbH
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_render_template]

# This file has been modified by Pierre Oberholzer to add support for payment_text_parser_git

import datetime
import json

import sys
import os
HOME_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, HOME_DIR)

from flask import Flask, render_template, jsonify, request, make_response
from flask_cors import CORS, cross_origin
from payment_text_parser.predict import get_pred_ptparser, get_pred_ptparser_wrapper, get_pred_tfidf,get_pred_ptparser_free_text

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

@app.route('/')
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]

    return render_template('index.html', times=dummy_times)

@app.route('/hello_world')
def hello_world():
    return 'Hello from payment_text_parser!'


@app.route('/pred_ptparser_wrapper',methods=['POST'])
@cross_origin()
def pred_ptparser_wrapper():

    #import pdb;pdb.set_trace()
    d_res = get_pred_ptparser_wrapper()
    return jsonify(d_res)

@app.route('/pred_ptparser',methods=['POST'])
@cross_origin()
def pred_ptparser():

    #import pdb;pdb.set_trace()
    d_res = get_pred_ptparser()
    #return jsonify(d_res)
    return make_response(jsonify(d_res), 200)

@app.route('/pred_ptparser_free_text',methods=['POST'])
@cross_origin()
def pred_ptparser_free_text():

    #import pdb;pdb.set_trace()
    d_res = get_pred_ptparser_free_text()
    #return jsonify(d_res)
    return make_response(jsonify(d_res), 200)

@app.route('/pred_tfidf',methods=['POST'])
@cross_origin()
def pred_tfidf():

    d_res = get_pred_tfidf()
    return jsonify(d_res)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.

    #app.run(host='127.0.0.1', port=8080, debug=False)
    app.run(debug=False, host='0.0.0.0', port=5000)
    #app.run()
# [START gae_python37_render_template]
