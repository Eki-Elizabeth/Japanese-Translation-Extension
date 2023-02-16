#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask,request
app = Flask(__name__)

@app.route('/test')
def test():
    return json.dumps({'name': 'testuser',
                       'email': 'testuser@outlook.com'})

@app.route('/api/translate', methods=['GET', 'POST'])
def translate():
    data = request.get_json()
    print(data['text'])  
    return json.dumps({'name': 'testuser',
                       'email': 'testuser@outlook.com'})
    
app.run()

