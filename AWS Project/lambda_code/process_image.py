import json
import boto3
import os
import urllib.parse

s3 = boto3.client('s3')
rek = boto3.client('rekognition')
ddb = boto3.resource('dynamodb')

TABLE_NAME = os.environ.get('table_name')
VALID_BUCKET = os.environ.get('bucket_name')

table = ddb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        for record in event['Records']:

            body = json.loads(record['body'])
            s3_event = body['Records'][0]['s3']

            bucket = s3_event['bucket']['name']
            key = urllib.parse.unquote_plus(s3_event['object']['key'])

            # Call Rekognition
            response = rek.detect_labels(
                Image={'S3Object': {'Bucket': bucket, 'Name': key}},
                MaxLabels=5
            )

            labels = [label['Name'] for label in response['Labels']]

            # Store metadata in DynamoDB
            table.put_item(
                Item={
                    'imageID': key,
                    'labels': labels
                }
            )

            s3.copy_object(
                Bucket=VALID_BUCKET,
                CopySource={'Bucket': bucket, 'Key': key},
                Key=key
            )

        return {
            "statusCode": 200,
            "body": json.dumps("Processing complete")
        }

    except Exception as e:
        print("ERROR:", str(e))
        raise e