# Picture captioning lambda function example

## What's this?

Picture captioning and tranlating labmda function, which get a caption of picture and translate it into Japanese text using two APIs, [Microsoft Compute Vision API](https://azure.microsoft.com/ja-jp/services/cognitive-services/computer-vision/) and [Microsoft Translator API](https://www.microsoft.com/ja-jp/translator/translatorapi.aspx).

## System requirements

- [serverless framework](https://github.com/serverless/serverless)
- python2.7 
- aws-cli

AWS user of serverless framework should have an AdministratorAccess permission. 

Also, you may have to create a profile for servelss framework.

```
$ aws configure --profile your_serverless_profile_name
```
 
## How to use

### Get API subscription keys

##### Microsoft Computer Vision API

[https://azure.microsoft.com/ja-jp/try/cognitive-services/?productId=%2Fproducts%2F54d873dd5eefd00dc474a0f4](https://azure.microsoft.com/ja-jp/try/cognitive-services/?productId=%2Fproducts%2F54d873dd5eefd00dc474a0f4)

##### Microsoft Translator API

[https://www.microsoft.com/ja-jp/translator/getstarted.aspx](https://www.microsoft.com/ja-jp/translator/getstarted.aspx)

### Configuration

Edit serverless.yml depending on your needs.

Default values are

- service name: PictureCaptioning
- stage name: dev
- function name: picture_caption
- path of http endpoint: pictures/caption

If you don't want to create AWS Gateway HTTP endpoints, please comment out `events` section.


### Setting up environment variables

- MS\_COGNITIVE\_VISION\_API\_KEY
- MS\_COGNITIVE\_TRANSLATE\_API\_KEY

Each variable should have a value of api key.

### Running local

```
$ sls invoke local -f picture_caption -d '{"queryStringParameters": {"url": your_picture_url }}'
```

Response sample is

```
{
    "body": "{\"url\": \"https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Ch_mtn_zoo_giraffes_2003.jpg/1200px-Ch_mtn_zoo_giraffes_2003.jpg\", 
              \"caption_en\": \"a group of giraffe standing on top of a dirt field\", 
              \"caption_ja\": \"\\u30c0\\u30fc\\u30c8\\u7551\\u306e\\u4e0a\\u306b\\u7acb\\u3064\\u30ad\\u30ea\\u30f3\\u306e\\u30b0\\u30eb\\u30fc\\u30d7\", 
              \"event\": {\"queryStringParameters\": {\"url\": \"https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Ch_mtn_zoo_giraffes_2003.jpg/1200px-Ch_mtn_zoo_giraffes_2003.jpg\"}}}",
    "statusCode": 200
}
```

### Deployment to AWS

#### Install dependencies

Install serverless-python-requirements package.

```
$ npm install 
```

#### Deployment

```
$ sls deploy -v --profile your_serverless_profile_name
```

Then, you can test your deployed lambda function.

```
$ sls invoke -f picture_caption -d '{"queryStringParameters": {"url": your_picture_url }}' --log
```
