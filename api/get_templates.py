import json
from dbLib.dblib import *
from S3Lib.s3_lib import get_file as signedURL
    
def get_gallery(event, context):
    templates = {str(n).zfill(2):signedURL(f'backgrounds/png/{str(n).zfill(2)}.png') for n in range(27)}
    return {
        'statusCode': 200,
        'body': json.dumps(templates)
    }

