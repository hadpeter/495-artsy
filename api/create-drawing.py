import json
import dblib
import time

def create_id(userId):
    return str(userId) + '-' + str(time.time_ns())

def binary_search(drawings):
    drawings.sort()
    index = len(drawings)+1
    if(index==1 or drawings[index-2]==index-1):
        return index
    low = 0
    high = index-1
    while(low!=high):
        index = (high+low)//2
        if(drawings[index]==index+1):
            low = index+1
        else:
            high=index
    return high+1

def next_greatest(drawings): #assumes only deletions and insertions without swapping
    index = 1
    length = len(drawings)
    if(length>0):
        index = drawings[length-1]+2
    return index

def lambda_handler(event, context):
    #drawingIds = dblib.get_user_attr(event['userId'],['drawings'])['drawings']
    dblib.create_drawing(event['userId'],create_id(event['userId']),event['template'],time.time_ns())
    #list = [1,2,3,5,6,7,8,9,10,12,13,14,15,16,17,18,19]
    return {
        'statusCode': 200,
        #'number': binary_search(list),
        #'drawingIds': create_id(event['userId']),
        'body': str(type(drawingIds))
    }
