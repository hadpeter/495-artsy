import json
from dblib import *
from s3_lib import get_file as signedURL
    
def get_templates(event, context):
    templates = {str(n).zfill(2):signedURL('artsy-bucket', f'backgrounds/png/{str(n).zfill(2)}.png') for n in range(1, 27) }
    return {
        'statusCode': 200,
        'body': json.dumps(templates)
    }
