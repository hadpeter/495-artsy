import json
import boto3
import requests


def lambda_handler(event, context):
    # construct location based on the api call and s3 folder structure
    location = 'artsy-bucket'
    desired_object = 'IMG_3192.jpeg'
    s3 = boto3.client('s3')
    #contents = s3.list_objects_v2(Bucket=location)
    url = s3.generate_presigned_url('get_object', Params = {'Bucket': location, 'Key': desired_object}, ExpiresIn = 100)
    #url = create_presigned_url('BUCKET_NAME', '')
    if url is not None:
        response = requests.get(url)
        print("Got response")
        print(response)
    
    #print(contents)
    print("results")
    # generate signed url
    signed_url = "testing"
    return {
        'statusCode': 200,
        'body': json.dumps(signed_url)
    }
    
def upload_file():
    object_name = 'OBJECT_NAME'
    response = create_presigned_post('BUCKET_NAME', object_name)
    if response is None:
        exit(1)
    with open(object_name, 'rb') as f:
        files = {'file': (object_name, f)}
        http_response = requests.post(response['url'], data=response['fields'], files=files)
    logging.info(f'http status code: {http_response.status_code}')
