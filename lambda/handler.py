import json
import os
from datetime import datetime
from hashlib import md5

import boto3

s3 = boto3.client('s3')

S3_OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']
S3_ERROR_BUCKET = os.environ['ERROR_BUCKET']

BASE_PREFIX = os.environ.get('BASE_PREFIX', '')


def prepare_statement(body):
    account = body['data']['account']
    statement = body['data']['statementItem']

    statement.update({
        'account': account
    })

    return statement


def make_prefix_from_timestamp(timestamp):
    unix_time = int(timestamp)
    return datetime.fromtimestamp(unix_time).strftime('%Y/%m')


def lambda_handler(event, context):
    raw_body = event['body'].encode('UTF-8')
    json_body = json.loads(raw_body)
    md5_hash = md5(raw_body).hexdigest()

    try:
        data = prepare_statement(json_body)
        dump_data = json.dumps(data).encode('UTF-8')
        key = f"{BASE_PREFIX}/{make_prefix_from_timestamp(data['time'])}/{md5_hash}.json"
        s3.put_object(Bucket=S3_OUTPUT_BUCKET, Key=key, Body=dump_data)

    except Exception as e:
        s3.put_object(Bucket=S3_ERROR_BUCKET, Key=f'errors/{md5_hash}.json', Body=raw_body)
        raise e

    return {
        'statusCode': 200,
    }
