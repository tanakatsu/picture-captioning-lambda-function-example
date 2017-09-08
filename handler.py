import vision_client
import translate_client
import synthesis_client
import s3_client
import os
import json
import datetime


def GetPictureCaption(event, context):
    print(event)
    # print(os.environ)

    try:
        # url = event["url"]  # if you don't use the http event with the LAMBDA-PROXY integration
        url = event["queryStringParameters"]["url"]
    except:
        url = None

    try:
        # url = event["voice"]  # if you don't use the http event with the LAMBDA-PROXY integration
        voice = event["queryStringParameters"]["voice"]
    except:
        voice = False

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

    if voice:
        key = os.environ['MS_COGNITIVE_SPEECH_API_KEY']
        syn_client = synthesis_client.SynthesisClient(api_key=key)
        voice_data = syn_client.synthesis(result_text)
        print('%d bytes' % len(voice_data))

        bucket = os.environ['S3_BUCKET']
        prefix_key = os.environ['S3_PREFIX_KEY']

        dt = datetime.datetime.now()
        key = '%d-%d-%d-%d-%d-%d.wav' % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        if prefix_key:
            key = prefix_key + '/' + key
        s3_cli = s3_client.S3Client()
        s3_cli.upload(bucket, key, voice_data)
        print('uploaded')
        speech_url = s3_cli.signed_url(bucket, key)
    else:
        speech_url = None

    result = {
        "url": url,
        "caption_en": caption,
        "caption_ja": result_text,
        "speech_url": speech_url,
        "event": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(result)
    }

    return response

    # return result  # if you don't use http event with the LAMBDA-PROXY integration
