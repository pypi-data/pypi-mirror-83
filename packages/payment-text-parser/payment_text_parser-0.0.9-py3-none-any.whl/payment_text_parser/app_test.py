# (C) Copyright 2020 Alpina Analytics GmbH
#
# Copyright 2015 Google Inc. All Rights Reserved.
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
#
# This file has been modified by Pierre Oberholzer to add support for payment_text_parser_git

from payment_text_parser import app


def test_index():
    app.app.testing = True
    client = app.app.test_client()

    r = client.get('/')
    assert r.status_code == 200

    r = client.get('/hello_world')
    assert r.data == b'Hello from payment_text_parser!'

    d_input = {"text":"Henry Meyar Bahnhofstrasse 1 8001 Zurich"}
    r = client.post('/parse', json=d_input)
    #r = client.post('/parse',data = json.dumps(d_input),content_type = 'application/json')
    json_data = r.get_json()
    #json_data = r.json
    print(json_data)
    #print(r.data)

test_index()