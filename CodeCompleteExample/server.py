#!/usr/bin/env python
# Copyright 2013 Abram Hindle
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
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask

import flask
from flask import Flask, request
import json
import difflib
app = Flask(__name__)
app.debug = True


def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data != ''):
        return json.loads(request.data)
    else:
        return json.loads(request.form.keys()[0])


ourwords = []

def load_words():
    global ourwords
    words = file("server.py").read().split()
    x = dict()
    for word in words:
        x[word] = 1
    ourwords = x.keys()
    ourwords.sort()

def get_closest_words(entity, n):
    global ourwords
    print(ourwords)
    return difflib.get_close_matches(entity, ourwords, n, 0.1)

@app.route("/")
def hello():
    return flask.redirect("/static/index.html")

@app.route("/words/<entity>")    
def get_words(entity):
    words = get_closest_words(entity, 10)
    #app.res.headers['Cache-Control'] = 'public'
    #return json.dumps(words)
    return (json.dumps(words), 200, {"Cache-Control":"public, max-age=360000", 
                                  "Content-type":"application/json"})

if __name__ == "__main__":
    load_words()
    app.run()
