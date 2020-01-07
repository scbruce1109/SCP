import boto3
import json
import os
import re
from django.conf import settings


# with open("creds.json", "r") as creds:
#     creds = json.load(creds)
#
# AWS_ACCESS_KEY_ID = creds.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = creds.get('AWS_SECRET_ACCESS_KEY')

class AWSDownload(object):
    access_key = None
    secret_key = None
    bucket = None
    expires = getattr(settings, 'AWS_DOWNLOAD_EXPIRE', 60)

    def __init__(self, access_key, secret_key, bucket, *args, **kwargs):
        self.bucket = bucket
        self.access_key = access_key
        self.secret_key = secret_key
        super(AWSDownload, self).__init__(*args, **kwargs)

    def s3connect(self):

        s3 = boto3.client('s3',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            )
        return s3

    def get_filename(self, path, new_filename=None):
        current_filename =  os.path.basename(path)
        if new_filename is not None:
            filename, file_extension = os.path.splitext(current_filename)
            escaped_new_filename_base = re.sub(
                                            '[^A-Za-z0-9\#]+',
                                            '-',
                                            new_filename)
            escaped_filename = escaped_new_filename_base + file_extension
            return escaped_filename
        return current_filename

    def generate_url(self, path, download=True, new_filename=None):
        s3 = self.s3connect()
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': self.bucket,
                'Key': path,
            },
            ExpiresIn=60
        )
        return url

# url = s3.generate_presigned_url(
#     ClientMethod='get_object',
#     Params={
#         'Bucket': 'ecommerce-243220',
#         'Key': 'protected/product/beat/1/SampleFlip7_13.mp3'
#     },
#     ExpiresIn=60
# )
# print(url)
