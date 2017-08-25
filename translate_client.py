import requests
import xml.etree.ElementTree as ET
import os

# http://taimi.hateblo.jp/entry/2017/02/05/204109

class TranslateClient():

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
        # print('token=', token)
        return token

    def translate(self, word):
        if not self.token:
            self.token = self.get_token()

        response = requests.get(
            'https://api.microsofttranslator.com/v2/http.svc/Translate',
            params={
                'appid': 'Bearer ' + self.token,
                'to': 'ja',
                'text': word,
                'category': 'generalnn'
            }
        ).text  # unicode

        translated_word = ET.fromstring(response.encode('utf-8')).text
        return translated_word


if __name__ == "__main__":
    word = "a group of giraffe standing on top of a dirt field"
    key = os.environ['MS_COGNITIVE_TRANSLATE_API_KEY']
    client = TranslateClient(api_key=key)
    result = client.translate(word)
    print(word)
    print('->')
    print(result)
