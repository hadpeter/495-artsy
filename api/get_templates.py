import json
from dblib import *
from s3lib import imgURL as signedURL
    
def get_gallery(event, context):
    templates = {str(n).zfill(2):signedURL(f'backgrounds/png/{str(n).zfill(2)}.png') for n in range(27)}
    return {
        'statusCode': 200,
        'body': json.dumps(templates)
    }

