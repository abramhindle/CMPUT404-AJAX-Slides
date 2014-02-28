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
app = Flask(__name__)
app.debug = True

class World:
    
    def __init__(self):
        self.clear()
        
    def update(self, entity, key, value):
        entry = self.space.get(entity,dict())
        entry[key] = value
        self.space[entity] = entry

    def set(self, entity, data):
        self.space[entity] = data
        self.notify_all(entity,data)

    def clear(self):
        self.space = dict()
        self.listeners = dict()

    def get(self, entity):
        return self.space.get(entity,dict())
    
    def world(self):
        return self.space

    def notify_all(self,entity,data):
        for listener in self.listeners:
           self.listeners[listener][entity] = data

    def add_listener(self,listener_name):
	self.listener[listener_name] = dict()

    def get_listener(self, listerner_name):
	return self.listener[listener_name]

# you can test
# curl -v   -H "Content-Type: appication/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}' 

myWorld = World()          

def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data != ''):
        return json.loads(request.data)
    else:
        return json.loads(request.form.keys()[0])

@app.route("/")
def hello():
    return "World Observer Framework!"

@app.route("/entity/<entity>", methods=['POST','PUT'])
def update(entity):
    v = flask_post_json()
    myWorld.set( entity, v )
    return flask.jsonify(myWorld.get(entity))

@app.route("/listener/<entity>", methods=['POST','PUT'])
def add_listener(entity):
    myWorld.add_listener( entity )
    return flask.jsonify(dict())

@app.route("/listener/<entity>")    
def get_listener(entity):
    return flask.jsonify(myWorld.get_listener(entity))


if __name__ == "__main__":
    app.run()
