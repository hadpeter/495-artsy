import json
from dblib import *
    
def add_tag(event, context):
    drawingId = event['headers']['drawingId']
    tag = event['headers']['drawingId']
    add_drawing_tag(drawingId, tag)
    return {
        'statusCode': 200
    }