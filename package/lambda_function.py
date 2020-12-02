import json
import apiLib


def lambda_handler(event, context):

    try:
        return apiLib.apiDict[event["resource"][1:]](event)
    except Exception as e:
        return {
            'statusCode': 420,
            'body': json.dumps(e.args)
        }