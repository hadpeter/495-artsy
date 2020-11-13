import json
from dbLib.dblib import *

def purchase_brush(event, context):
    userId = event['headers']['userId']
    brushId = event['headers']['brushId']
    cost = event['headers']['cost']
    add_coins(userId, cost*(-1))
    add_brush(userId, brushId)
    return {
        'statusCode': 200,
    }

