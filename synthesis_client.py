# -*- coding: utf-8 -*-
import os
import requests
import subprocess


class SynthesisClient():

    def __init__(self, api_key=None):
        self.key = api_key
        self.token = None

    def get_token(self):
        token = requests.post(
            'https://api.cognitive.microsoft.com/sts/v1.0/issueToken',
            params={
                'Subscription-Key': self.key
            }
        ).text
        return token

    def synthesis(self, text):
        if not self.token:
            self.token = self.get_token()

        ssml = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="ja-JP"><voice xml:lang="ja-JP" name="Microsoft Server Speech Text to Speech Voice (ja-JP, Ayumi, Apollo)">' + text + '</voice></speak>'
        payload = ssml

        headers = {'content-type': 'application/ssml+xml',
                   'X-Microsoft-OutputFormat': 'riff-16khz-16bit-mono-pcm',
                   'Authorization': 'Bearer ' + self.token}

        response = requests.post(
            'https://speech.platform.bing.com/synthesize',
            data=payload,
            headers=headers
        )

        # print(response.status_code)
        if response.status_code == requests.codes.ok:
            # print(response.headers)
            voice = response.content
            return voice
        else:
            print(response.text)

if __name__ == "__main__":
    text = u'こんにちは'
    key = os.environ['MS_COGNITIVE_SPEECH_API_KEY']
    client = SynthesisClient(api_key=key)
    result = client.synthesis(text)
    with open('output_voice.wav', 'wb') as f:
        f.write(result)
    subprocess.call(['afplay', 'output_voice.wav'])
