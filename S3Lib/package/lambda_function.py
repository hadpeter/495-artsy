import json
import boto3
import requests


def lambda_handler(event, context):
    print(context)
    print("event")
    
    # get_url = get_file()
    post_url = upload_file(event['img'])
    return {
        'statusCode': 200,
        'body': json.dumps(post_url)
    }
    
def upload_file(input_img):
    # to generate url that can be used to make a post to the s3 bucket
    bucket_name = 'artsy-bucket'
    obj_name = input_img
    s3 = boto3.client('s3')
    response = s3.generate_presigned_post(bucket_name, obj_name)
    #error handling
    if response is None:
        exit(1)
    print(response['url'])
    # outline of how the api will use the url to make a post
    # with open(obj_name, 'rb') as i:
        # files = {'file': (object_name, i)}
         # http_response = requests.post(response['url'], data=response['fields'], files=files)
    # print('http status code: {http_response.status_code}')
    return response

def get_file():
    # construct location based on the api call and s3 folder structure
    bucket_name = 'artsy-bucket'
    desired_object = 'IMG_3192.jpeg'
    s3 = boto3.client('s3')
    url = s3.generate_presigned_url('get_object', Params = {'Bucket': bucket_name, 'Key': desired_object}, ExpiresIn = 100)
    if url is None:
        print("failure generating presigned url")
        exit(1)
    return url