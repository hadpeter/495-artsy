import json
from dbLib.dblib import *

def get_user_info(event, context):
    userId = event['headers']['userId']
    attrs = ["userId", "coins", "brushes", "paints", "baseline", "breathCount", "backgrounds", "drawings", "unlimitedExpiration"]
    user_info = get_user_attr(userId, attrs)
    return {
        'statusCode': 200,
        'body': json.dumps(user_info)
    }

