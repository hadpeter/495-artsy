import json
from dblib import *

class GetUserInfoError(Exception):
    """Exception raised for errors in the get_user_info endpoint.

    Attributes:
        headers -- headers passed from the HTTP request
        message -- explanation of the error
    """

    def __init__(self, message="error in /get-user-info"):
        self.message = message
        super().__init__(self.message)

def get_user_info(event, context):
    if "headers" not in event.keys():
        raise GetUserInfoError(message"headers not found")
    if "userId" not in event["headers"]:
        raise GetUserInfoError(message"userId not found in headers")
    userId = event['headers']['userId']
    attrs = ["userId", "coins", "brushes", "paints", "baseline", "history", "backgrounds", "drawings", "lastBreath"]
    user_info = get_user_attr(userId, attrs)
    if user_info is None:
        raise GetUserInfoError(message"userId does not exist")
    return {
        'statusCode': 200,
        'body': json.dumps(user_info)
    }

