import json
import s3_lib
import dblib

def lambda_handler(event, context):
    response = s3_lib('artsy-bucket',event['drawingId'])
    dblib.set_titel(event['drawingId'],event['title'])
    return {
        'statusCode': 200,
        'body': json.dumps(response),
        'png':str(event['drawingId'])+".png",
        'svg': str(event['drawingId'])+".svg"
    }
