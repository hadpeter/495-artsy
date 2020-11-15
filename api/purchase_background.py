import json
from dbLib.dblib import *

def purchase_background(event, context):
    userId = event['headers']['userId']
    backgroundId = event['headers']['backgroundId']
    cost = event['headers']['cost']
    add_coins(userId, cost*(-1))
    add_background(userId, backgroundId)
    return {
        'statusCode': 200,
    }