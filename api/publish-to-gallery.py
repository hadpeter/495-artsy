import json
from dblib import *

class PublishToGalleryError(Exception):
    """Exception raised for errors in the get_user_info endpoint.

    Attributes:
        headers -- headers passed from the HTTP request
        message -- explanation of the error
    """

    def __init__(self, headers={}, message="error in /get-user-info"):
        self.headers = headers
        self.message = message
        super().__init__(self.message)

def get_user_info(event, context):
    if "headers" not in event.keys():
        raise PublishToGalleryError(message"headers not found")
    if "drawingId" not in event["headers"] or "title" not in event["headers"]:
        raise PublishToGalleryError(message"invalid or missing headers")
    drawingId = event['headers']['drawingId']
    title = event['headers']['title']
    try:
        set_title(drawingId, title)
        publish_drawing(drawingId)
    except Exception as e:
        raise
    return {
        'statusCode': 200
    }
