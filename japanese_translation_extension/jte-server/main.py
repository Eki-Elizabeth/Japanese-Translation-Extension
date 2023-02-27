#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask,request,send_file
from flask_cors import CORS, cross_origin
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import boto3
import os,io
import sys
import subprocess
from tempfile import gettempdir


app = Flask(__name__)
CORS(app, support_credentials=True)

def get_voice(s):

    # Create a client using the credentials and region defined in the [adminuser]
    # section of the AWS credentials file (~/.aws/credentials).
    session = Session(profile_name="default")
    polly = session.client("polly")

    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=s, OutputFormat="mp3",
                                            VoiceId="Mizuki")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        return response["AudioStream"]
            #with closing(response["AudioStream"]) as stream:
                #output = os.path.join(gettempdir(), "speech.mp3")

               #try:
                # Open a file for writing the output as a binary stream
               #     with open(output, "wb") as file:
               #        file.write(stream.read())
               #except IOError as error:
                  # Could not write to file, exit gracefully
               #   print(error)
               #   sys.exit(-1)

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        #sys.exit(-1)
        return None


@app.route('/test')
def test():
    return json.dumps({'name': 'testuser',
                       'email': 'testuser@outlook.com'})

@app.route('/api/translate', methods=['GET', 'POST'])
def translate():
    data = request.get_json()
    translate = boto3.client(service_name='translate', region_name='us-west-1', use_ssl=True)
    result = translate.translate_text(Text=data['text'], SourceLanguageCode="ja", TargetLanguageCode="zh")
    print(json.dumps({'text': result.get('TranslatedText')}))
    print(json.dumps({'text': result.get('TranslatedText')}))
    return json.dumps({'text': result.get('TranslatedText')})



@app.route('/api/voice', methods=['GET'])
def voice():
    #data = request.get_json()
    v = get_voice(request.args.get('text'))

    content = v.read()

    return send_file(
        io.BytesIO(content),
        download_name='logo.mp3',
        mimetype='audio/mpeg'
    )
    
app.run()    