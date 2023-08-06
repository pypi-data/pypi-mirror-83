# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import setuptools

# Libraries from requirements.txt to be skipeed
skip_libs = ['matplotlib','shap']

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#") and all([True if lib not in line else False for lib in skip_libs])]

install_reqs = parse_requirements('requirements.txt')

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="payment_text_parser",
    version="0.0.9",
    author="Pierre Oberholzer",
    author_email="pierre.oberholzer@alpina-analytics.com",
    description="Parser for entity/address free text (based on libpostal/spacy)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/alpina-analytics/payment_text_parser.git",
    include_package_data=True,  # Needed to include configs from MANIFEST.in
    #packages=setuptools.find_packages(),
    #package_dir = {'': 'payment_text_parser'},
    #packages = setuptools.find_packages(where = '.', exclude=["payment_text_parser/tests"]),
    packages = setuptools.find_packages(where = '.',exclude=[
        "payment_text_parser.tests",
        "payment_text_parser.core_nlp"
    ]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent"
    ],
    install_requires=install_reqs

)