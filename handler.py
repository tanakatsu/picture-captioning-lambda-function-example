import vision_client
import translate_client
import os
import json


def GetPictureCaption(event, context):
    print(event)

    try:
        # url = event["url"]  # if you don't use the http event with the LAMBDA-PROXY integration
        url = event["queryStringParameters"]["url"]
    except:
        url = None

    # url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Ch_mtn_zoo_giraffes_2003.jpg/1200px-Ch_mtn_zoo_giraffes_2003.jpg"
    print('url=', url)

    if not url:
        result = {
            "url": url,
            "event": event
        }
        response = {
            "statusCode": 200,
            "body": result
        }
        return response

    key = os.environ['MS_COGNITIVE_VISION_API_KEY']

    v_client = vision_client.VisionClient(api_key=key)
    result = v_client.get_labels(url)
    print(result)

    caption = result['description']['captions'][0]['text']
    print(caption)

    key = os.environ['MS_COGNITIVE_TRANSLATE_API_KEY']
    t_client = translate_client.TranslateClient(api_key=key)
    result_text = t_client.translate(caption)

    result_text = result_text.encode('utf-8')
    print(result_text)

    result = {
        "url": url,
        "caption_en": caption,
        "caption_ja": result_text,
        "event": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(result)
    }

    return response

    # return result  # if you don't use http event with the LAMBDA-PROXY integration
