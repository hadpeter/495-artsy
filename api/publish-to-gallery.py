import json
from dbLib.dblib import *

def get_user_info(event, context):
    drawingId = event['headers']['drawingId']
    title = event['headers']['title']
    set_title(drawingId, title)
    publish_drawing(drawingId)
    return {
        'statusCode': 200
    }
