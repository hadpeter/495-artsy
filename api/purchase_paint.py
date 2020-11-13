import json
from dbLib.dblib import *

def purchase_paint(event, context):
    userId = event['headers']['paintId']
    paintId = event['headers']['paintId']
    cost = event['headers']['cost']
    add_coins(userId, cost*(-1))
    add_paint(userId, paintId)
    return {
        'statusCode': 200,
    }