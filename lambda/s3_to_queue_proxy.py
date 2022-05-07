import os
import urllib

import boto3

s3 = boto3.client('s3')
sqs = boto3.client('sqs')

QUEUE_URL = os.environ['QUEUE_URL']


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    # assume only 1 object per invoke
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='UTF-8')

    response = s3.get_object(Bucket=bucket, Key=key)
    data = response['Body'].read().decode()

    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=data
    )
