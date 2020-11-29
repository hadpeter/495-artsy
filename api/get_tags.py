import json
from dblib import *
    
def get_tags(event, context):
    drawingId = event['headers']['drawingId']
    tags = get_drawing_tags(drawingId)
    return {
        'statusCode': 200,
        'body': json.dumps(tags)
    }
