import json
import math
import boto3
from dblib import *
import time
import s3_lib

def get_user_info(event):
    userId = event['headers']['userId']
    attrs = ["userId", "coins", "brushes", "paints", "baseline", "breathCount", "backgrounds", "drawings", "unlimitedExpiration"]
    user_info = get_user_attr(userId, attrs)
    
    #fix number issues
    user_info["coins"] = int(user_info["coins"])
    user_info["breathCount"] = int(user_info["breathCount"])
    user_info["unlimitedExpiration"] = int(user_info["unlimitedExpiration"])
    user_info["baseline"] = int(user_info["baseline"])
    return {
        'statusCode': 200,
        'body': json.dumps(user_info)
    }


def get_user_art(event):
    userId = event["headers"]["userId"]
    data = fetch_user_art_all(userId)
    canvas = []
    template = []

    for drawing in data:
        new_item = {
            "png": s3_lib.get_file('artsy-bucket', f'drawings/{userId}/png/{drawing["drawingId"]}.png'),
            "svg": s3_lib.get_file('artsy-bucket', f'drawings/{userId}/svg/{drawing["drawingId"]}.svg'),
            "drawingId": drawing["drawingId"],
            "time": int(drawing["modified"])
        }

        if drawing["coloringPage"] != "":
            new_item['templateUrl'] = s3_lib.get_file('artsy-bucket', f'backgrounds/svg/{drawing["coloringPage"]}.svg')
            template.append(new_item)
        else:
            canvas.append(new_item)
    response = {
        "canvas": canvas,
        "template": template
    }

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


def api_create_user(event):
    deviceId = event["headers"]["deviceId"]
    userId = event["headers"]["deviceId"] + "-" + str(time.time_ns())
    create_user(deviceId, userId)
    return {
        'statusCode': 200,
        'body': json.dumps(userId)
    }

def api_get_user_id(event):
    deviceId = event["headers"]["deviceId"]
    userId = get_user_id(deviceId)
    return {
        'statusCode': 200,
        'body': json.dumps(userId)
    }
    


def get_drawing(event):
    drawingId = event["headers"]['drawingId']
    userId = '-'.join(event["headers"]['drawingId'].split('-')[0:2])

    response = {
        "png": s3_lib.get_file('artsy-bucket', f'drawings/{userId}/png/{drawingId}.png'),
        "svg": s3_lib.get_file('artsy-bucket', f'drawings/{userId}/svg/{drawingId}.svg')
    }

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


def get_templates(event):
    response = {
            "templates": [{"title": str(n).zfill(2), "url": s3_lib.get_file('artsy-bucket', f'backgrounds/png/{str(n).zfill(2)}.png')} for n in range(1, 27) ]
    }

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def api_create_drawing(event):
    drawingId = create_id(event['headers']['userId'])
    if 'template'in event['headers']:
        create_drawing(event['headers']['userId'], drawingId ,event['headers']['template'],time.time_ns())
    else:
        create_drawing(event['headers']['userId'], drawingId, "", time.time_ns())
    return {
        'statusCode': 200,
        'body': json.dumps(drawingId)
    }

def save_drawing(event):
    drawingId = event["headers"]['drawingId']
    userId = '-'.join(event["headers"]['drawingId'].split('-')[0:2])

    if "title" in event["headers"]:
        set_title(event["headers"]['drawingId'],event["headers"]['title'])

    response = {
        "png": s3_lib.upload_file('artsy-bucket', f'drawings/{userId}/png/{drawingId}.png'),
        "svg": s3_lib.upload_file('artsy-bucket', f'drawings/{userId}/svg/{drawingId}.svg')
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


def purchase_brush(event):
    userId = event['headers']['userId']
    brushId = event['headers']['brushId']
    cost = int(event['headers']['cost'])
    add_coins(userId, cost*(-1))
    add_brush(userId, brushId)
    return {
        'statusCode': 200,
    }


def purchase_paint(event):
    userId = event['headers']['userId']
    paintId = event['headers']['paintId']
    cost = int(event['headers']['cost'])
    add_coins(userId, cost*(-1))
    add_paint(userId, paintId)
    return {
        'statusCode': 200,
    }


def purchase_background(event):
    userId = event['headers']['userId']
    backgroundId = event['headers']['backgroundId']
    cost = int(event['headers']['cost'])
    add_coins(userId, cost*(-1))
    add_background(userId, backgroundId)
    return {
        'statusCode': 200,
    }

def get_gallery(event):
    canvases = fetch_gallery_canvases()
    canvases = sorted(canvases, key = lambda i: i['modified'],reverse=True)
    canvases = map(image_object, canvases)
    templates = fetch_gallery_coloringPages()
    templates = sorted(templates, key = lambda i: i['modified'],reverse=True)
    templates = map(image_object, templates)
    response = {
        "canvases": list(canvases),
        "templates": list(templates)
    }
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


def publish_to_gallery(event):
    drawingId = event['headers']['drawingId']
    title = event['headers']['title']
    set_title(drawingId, title)
    publish_drawing(drawingId)
    return {
        'statusCode': 200
    }

def api_add_breath(event):
    currTime = time.time_ns()
    userId = event['headers']['userId']
    flow = flow = [int(s) for s in event['headers']['flow'].split() if s.isdigit()]
    volume = [int(s) for s in event['headers']['volume'].split() if s.isdigit()]
    score = 0
    grade = ""
    feedback = ""
    legalBreath = True
    for num in flow:
        if num > 3:
            legalBreath = False
            break
    for num in volume:
        if num > 10:
            legalBreath = False
            break

    if legalBreath:
        breath = [currTime,flow,volume]
        add_raw_breath(userId,breath)
        [score,grade,feedback] = compute_score(flow,volume)
        baseline = get_user_attr(userId, ["baseline"])['baseline']
        LOWBAR = 0.4
        #LOWBAR = 0 #TEST VALUE
        UNLIMITED_DURATION = 3600000000000 #one hour in nanoseconds
        #UNLIMITED_DURATION = 10000000000 #10 seconds in nanoseconds | TEST VALUE
        
        if(score > LOWBAR*float(baseline)):
            if(get_user_attr(userId,['unlimitedExpiration'])['unlimitedExpiration']<currTime):
                add_breath(userId)
                if(get_user_attr(userId,['breathCount'])['breathCount']==10):
                    set_unlimited(userId, currTime+UNLIMITED_DURATION)
            add_coins(userId,score)
        if(score > baseline):
            set_baseline(userId,score)
    else:
        grade = "Ungraded"
        feedback = "There was an illegal integer in the flow/volume"
        
    response = {
        #'seconds_until_use': int((get_user_attr(event['headers']['userId'],['unlimitedExpiration'])['unlimitedExpiration']-time.time_ns())/1000000000),
        'grade': grade,
        'feedback': feedback,
        'score': score,
        'balance': int(get_user_attr(userId,['coins'])['coins']),
        'breathCount': int(get_user_attr(userId,['breathCount'])['breathCount'])
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def get_tags(event, context):
    drawingId = event['headers']['drawingId']
    tags = get_drawing_tags(drawingId)
    return {
        'statusCode': 200,
        'body': json.dumps(tags)
    }

def add_tag(event, context):
    drawingId = event['headers']['drawingId']
    tag = event['headers']['drawingId']
    add_drawing_tag(drawingId, tag)
    return {
        'statusCode': 200
    }


#Helper functions
def create_id(userId):
    return str(userId) + '-' + str(time.time_ns())

def image_object(img):
    userId = '-'.join(img['drawingId'].split('-')[0:2])

    response = {
        "imageUrl": s3_lib.get_file('artsy-bucket', f'drawings/{userId}/png/{img["drawingId"]}.png'),
        "title": img['title']
    }
    
    return response

def compute_score(flow,volume):
    weights = [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    values = [0,.5,.3,.1,0,1,.5,.3,0,1.1,.9,.2,0,1.2,.6,.5]
    length = len(flow)
    score = 0
    if(length<10):
        score = 20.0/(1+math.exp(-.47*(length-10)))
    else:
        score = 50.0/(1+math.exp(-.187*(length-10)))-15.0
    numerator = 0.0
    denominator = 0.0
    index = 0
    for x in range(length):
        numerator += values[4*index+flow[x]]
        denominator += weights[4*index+flow[x]]
        index = flow[x]
    if denominator == 0:
        denominator = 1
    modifier = numerator/denominator
    score = int(2*score*modifier)
    feedback = "Great form!"
    if modifier < .75:
        feedback = "Try breathing in more slowly!"
    elif length < 15:
        feedback = "Try taking longer breathes!"
    grade = "Needs Improvement"
    if score > 70:
        grade = "Fantastic"
    elif score > 50:
        grade = "Excellent"
    elif score > 30:
        grade = "Good"
    elif score > 10:
        grade = "Okay"
    return [score,grade,feedback]

apiDict = {
    "get-user-info": get_user_info,
    "get-user-art": get_user_art,
    "create-user": api_create_user,
    "get-drawing": get_drawing,
    "get-templates": get_templates,
    "create-drawing": api_create_drawing,
    "save-drawing": save_drawing,
    "purchase-brush": purchase_brush,
    "purchase-palette": purchase_paint,
    "purchase-background": purchase_background,
    "get-gallery": get_gallery,
    "publish-to-gallery": publish_to_gallery,
    "add-breath": api_add_breath
}