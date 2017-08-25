import httplib, urllib, base64, json
import os

# https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts/python

class VisionClient:

    def __init__(self, api_key=None):
        self.subscription_key = api_key

    def get_labels(self, url):
        uri_base = 'westcentralus.api.cognitive.microsoft.com'
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.subscription_key,
        }

        params = urllib.urlencode({
            # Request parameters. All of them are optional.
            'visualFeatures': 'Categories,Description,Color',
            'language': 'en',
        })

        body = json.dumps({"url": url})
        # print(body)

        try:
            # Execute the REST API call and get the response.
            conn = httplib.HTTPSConnection(uri_base)
            conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
            response = conn.getresponse()
            data = response.read()

            # print(data)
            parsed = json.loads(data.decode('utf-8'))
            # print ("Response:")
            # print (json.dumps(parsed, sort_keys=True, indent=2))
            conn.close()
        except Exception as e:
            print('Error:')
            print(e)

        return parsed

if __name__ == "__main__":
    url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Ch_mtn_zoo_giraffes_2003.jpg/1200px-Ch_mtn_zoo_giraffes_2003.jpg"
    key = os.environ['MS_COGNITIVE_VISION_API_KEY']
    client = VisionClient(api_key=key)
    print(client.get_labels(url))
