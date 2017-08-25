import vision_client
import translate_client
import os

def GetPictureCaption(event, context):
    print(event)

    if 'url' in event:
        url = event['url']
    else:
        url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Ch_mtn_zoo_giraffes_2003.jpg/1200px-Ch_mtn_zoo_giraffes_2003.jpg"
    print('url=', url)

    key = os.environ['MS_COGNITIVE_VISION_API_KEY']

    v_client = vision_client.VisionClient(api_key=key)
    result = v_client.get_labels(url)
    # print(result)

    caption = result['description']['captions'][0]['text']
    print(caption)

    key = os.environ['MS_COGNITIVE_TRANSLATE_API_KEY']
    t_client = translate_client.TranslateClient(api_key=key)
    result_text = t_client.translate(caption)

    result_text = result_text.encode('utf-8')
    print(result_text)

    return {
        "url": url,
        "caption_en": caption,
        "caption_ja": result_text,
        "event": event
    }
