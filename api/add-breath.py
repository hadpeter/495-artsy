import json
import dblib
import time
import random #TODO remove all random calls

def compute_score(flow,volume):
    weights = [0,1,1,1,1,1,1,1,1,1,1,1,1]
    values = [0,.5,.3,.1,0,1,.5,.3,0,1.1,.9,.2,0,1.2,.6,.5]
    length = len(flow)
    score = 0
    if(length<10):
        score = 52.0/(1+math.exp(-.39*(length-10)))
    else:
        score = 50.0/(1+math.exp(-.15*(length-10)))
    numerator = 0.0
    denominator = 0.0
    index = 0
    for x in range(length):
        numerator += values[4*index+flow[x]]
        denominator += weights[4*index+flow[x]]
        index = flow[x]
    if denominator == 0:
        denominator = 1
    return int(2*score*numerator/denominator)

def lambda_handler(event, context):
    currTime = time.time_ns()
    breath = [currTime,event['flow'],event['volume']]
    dblib.add_raw_breath(event['userId'],breath)
    score = compute_score(event['flow'],event['volume'])
    baseline = dblib.get_user_attr(event['userId'], ["baseline"])['baseline']
    LOWBAR = 0.4
    #LOWBAR = 0 #TEST VALUE
    UNLIMITED_DURATION = 3600000000000 #one hour in nanoseconds
    #UNLIMITED_DURATION = 10000000000 #10 seconds in nanoseconds | TEST VALUE
    
    if(score > LOWBAR*baseline):
        if(dblib.get_user_attr(event['userId'],['unlimitedExpiration'])['unlimitedExpiration']<currTime):
            dblib.add_breath(event['userId'])
            if(dblib.get_user_attr(event['userId'],['breathCount'])['breathCount']==10):
                dblib.set_unlimited(event['userId'], currTime+UNLIMITED_DURATION)
        dblib.add_coins(event['userId'],score)
    if(score > baseline):
        dblib.set_baseline(event['userId'],score)
    
    return {
        'statusCode': 200,
        'seconds until use': (dblib.get_user_attr(event['userId'],['unlimitedExpiration'])['unlimitedExpiration']-time.time_ns())/1000000000,
        'balance': dblib.get_user_attr(event['userId'],['coins'])['coins'],
        'breathCount': dblib.get_user_attr(event['userId'],['breathCount'])['breathCount']
    }