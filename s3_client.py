import boto3
from boto3.session import Session


class S3Client():

    def __init__(self, access_key=None, secret_key=None):
        self.access_key = access_key
        self.secret_key = secret_key

        if self.access_key and self.secret_key:
            session = Session(aws_access_key_id=self.access_key,
                              aws_secret_access_key=self.secret_key)
            self.resource = session.resource('s3')
            self.client = session.client('s3')
        else:
            self.resource = boto3.resource('s3')
            self.client = boto3.client('s3')

    def upload(self, bucket, key, data):
        s3 = self.resource
        s3.Object(bucket, key).put(Body=data, ContentType='audio/wav')

    def signed_url(self, bucket, key):
        s3 = self.client
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket,
                'Key': key
            }
        )
        return url
