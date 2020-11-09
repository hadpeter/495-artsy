import json
import boto3

def lambda_handler(event, context):
    # parse context for drawing id - api specific
    # read from s3
    location = 'artsy-bucket'
    s3 = boto3.client('s3')
    contents = s3.list_objects_v2(Bucket=location)
    
    print(contents)
    print("results")
    # generate signed url
    signed_url = "testing"
    return {
        'statusCode': 200,
        'body': json.dumps(signed_url)
    }

