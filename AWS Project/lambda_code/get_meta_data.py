import json
import boto3
import os

ddb = boto3.resource('dynamodb')

TABLE_NAME = os.environ.get('table_name')
table = ddb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        params = event.get('queryStringParameters') or {}
        image_id = params.get('imageID')

        if not image_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing imageID"})
            }

        response = table.get_item(
            Key={
                "imageID": image_id
            }
        )

        item = response.get('Item')

        if not item:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Not found"})
            }

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(item)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }