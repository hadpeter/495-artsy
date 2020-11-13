import json
import boto3
import requests

    
# bucket_name should be 'artsy-bucket' and the obj_name should specify the object
# in the bucket that we wish to generate a url to upload to
def upload_file(bucket_name, obj_name):
    s3 = boto3.client('s3')
    response = s3.generate_presigned_post(bucket_name, obj_name)
    #error handling
    if response is None:
        print("error generating url")
        raise Exception
    return response

# bucket_name should be 'artsy-bucket' and the obj_name should specify the object
# in the bucket that we wish to generate a url to access
def get_file(bucket_name , obj_name):
    s3 = boto3.client('s3')
    url = s3.generate_presigned_url('get_object', Params = {'Bucket': bucket_name, 'Key': obj_name}, ExpiresIn = 100)
    if url is None:
        print("failure generating presigned url")
        raise Exception
    return url

## Additional notes on usage
# for the url generated bu upload_file that is returned to the frontend, a post should be 
# made to it like the code bellow
# outline of how the api will use the url to make a post
    # with open(obj_name, 'rb') as i:
    #     files = {'file': (obj_name, i)}
    #     http_response = requests.post(response['url'], data=response['fields'], files=files)