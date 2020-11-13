import json
import apiLib
from apiLib import apiDict

def lambda_handler(event, context):

	try:
		return apiDict[event["resource"][1:](event)]
	except Exception as e:
		return {
        'statusCode': 420,
        'body': json.dumps(e)
    }


