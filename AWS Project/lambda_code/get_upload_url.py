import json
import boto3
import os
import uuid

s3 = boto3.client('s3')

BUCKET = os.environ.get('bucket')

def lambda_handler(event, context):
    try:
        params = event.get('queryStringParameters') or {}

        original_name = params.get('filename', 'upload.jpg')

        file_id = str(uuid.uuid4())
        key = f"uploads/{file_id}-{original_name}"

        # Generate presigned URL
        url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': BUCKET,
                'Key': key,
                'ContentType': 'image/jpeg'
            },
            ExpiresIn=600
        )

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "uploadUrl": url,
                "key": key
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }