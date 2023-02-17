#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask,request
import boto3
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/test')
def test():
    return json.dumps({'name': 'testuser',
                       'email': 'testuser@outlook.com'})

@app.route('/api/translate', methods=['GET', 'POST'])
def translate():
    data = request.get_json()
    translate = boto3.client(service_name='translate', region_name='us-west-1', use_ssl=True)
    result = translate.translate_text(Text=data['text'], SourceLanguageCode="en", TargetLanguageCode="de")
    print(json.dumps({'text': result.get('TranslatedText')}))
    print(json.dumps({'text': result.get('TranslatedText')}))
    return json.dumps({'text': result.get('TranslatedText')})
                       
app.run()

