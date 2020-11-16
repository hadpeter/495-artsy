import json
import dblib
import time
import random #TODO remove all random calls

def compute_score(flow,volume):
    #TODO implement something that actually analyses volume and flow
    return random.randint(50,50)

def lambda_handler(event, context):
    #dblib.create_user(event['userId'])
    score = compute_score(event['flow'],event['volume'])
    baseline = dblib.get_user_attr(event['userId'], ["baseline"])['baseline']
    #LOWBAR = 0.4
    LOWBAR = 0 #TEST VALUE
    #UNLIMITED_DURATION = 3600000000000 #one hour in nanoseconds
    UNLIMITED_DURATION = 10000000000 #10 seconds in nanoseconds | TEST VALUE
    
    if(score > LOWBAR*baseline):
        if(dblib.get_user_attr(event['userId'],['unlimitedExpiration'])['unlimitedExpiration']<time.time_ns()):
            dblib.add_breath(event['userId'])
            if(dblib.get_user_attr(event['userId'],['breathCount'])['breathCount']==10):
                dblib.set_unlimited(event['userId'], time.time_ns()+UNLIMITED_DURATION)
        dblib.add_coins(event['userId'],score)
    if(score > baseline):
        dblib.set_baseline(event['userId'],score)
    
    return {
        'statusCode': 200,
        'seconds until use': (dblib.get_user_attr(event['userId'],['unlimitedExpiration'])['unlimitedExpiration']-time.time_ns())/1000000000,
        'balance': dblib.get_user_attr(event['userId'],['coins'])['coins'],
        'breathCount': dblib.get_user_attr(event['userId'],['breathCount'])['breathCount']
    }