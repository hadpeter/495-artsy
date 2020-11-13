import json
from dblib import *
from s3_lib import get_file as signedURL
    
def get_templates(event, context):
    paths = {
        "01": signedURL('artsy-bucket', f'backgrounds/png/01.svg'),
        "02": signedURL('artsy-bucket', f'backgrounds/png/01.svg'),
        "03": signedURL('artsy-bucket', f'backgrounds/png/02.svg'),
        "04": signedURL('artsy-bucket', f'backgrounds/png/03.svg'),
        "05": signedURL('artsy-bucket', f'backgrounds/png/04.svg'),
        "06": signedURL('artsy-bucket', f'backgrounds/png/05.svg'),
        "07": signedURL('artsy-bucket', f'backgrounds/png/06.svg'),
        "08": signedURL('artsy-bucket', f'backgrounds/png/07.svg'),
        "09": signedURL('artsy-bucket', f'backgrounds/png/08.svg'),
        "10": signedURL('artsy-bucket', f'backgrounds/png/09.svg'),
        "11": signedURL('artsy-bucket', f'backgrounds/png/10.svg'),
        "12": signedURL('artsy-bucket', f'backgrounds/png/11.svg'),
        "13": signedURL('artsy-bucket', f'backgrounds/png/12.svg'),
        "14": signedURL('artsy-bucket', f'backgrounds/png/13.svg'),
        "15": signedURL('artsy-bucket', f'backgrounds/png/14.svg'),
        "16": signedURL('artsy-bucket', f'backgrounds/png/15.svg'),
        "17": signedURL('artsy-bucket', f'backgrounds/png/16.svg'),
        "18": signedURL('artsy-bucket', f'backgrounds/png/17.svg'),
        "19": signedURL('artsy-bucket', f'backgrounds/png/18.svg'),
        "20": signedURL('artsy-bucket', f'backgrounds/png/19.svg'),
        "21": signedURL('artsy-bucket', f'backgrounds/png/20.svg'),
        "22": signedURL('artsy-bucket', f'backgrounds/png/22.svg'),
        "23": signedURL('artsy-bucket', f'backgrounds/png/23.svg'),
        "24": signedURL('artsy-bucket', f'backgrounds/png/24.svg'),
        "25": signedURL('artsy-bucket', f'backgrounds/png/25.svg'),
        "26": signedURL('artsy-bucket', f'backgrounds/png/26.svg')
    }
    return {
        'statusCode': 200,
        'body': json.dumps(paths)
    }
