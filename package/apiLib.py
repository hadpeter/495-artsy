import json
import math
import boto3
from dblib import *
import time
import s3_lib


def get-user-info(event):
	userId = event['headers']['userId']
    attrs = ["userId", "coins", "brushes", "paints", "baseline", "breathCount", "backgrounds", "drawings", "unlimitedExpiration"]
    user_info = get_user_attr(userId, attrs)
    return {
        'statusCode': 200,
        'body': json.dumps(user_info)
    }


def get-user-art(event):
	userId = event["queryStringParameters"]["userId"]
	data = fetch_user_art_all(userId)
	canvas = []
	template = []

	for drawing in data:
		new_item = {
			"png": s3_lib.getfile('artsy-bucket', f'drawings/{userId}/{drawing["drawingId"]}.png'),
			"svg": s3_lib.getfile('artsy-bucket', f'drawings/{userId}/{drawing["drawingId"]}.svg'),
			"drawingId": drawing["drawingId"],
			"time": drawing["modified"]
		}

		if drawing["coloringPage"]:
			new_item['templateUrl'] = s3_lib.getfile('artsy-bucket', f'backgrounds/{img['drawingId']}.png')
			template.append(new_item)
		else:
			canvas.append(new_item)

	response = {
        "canvas": canvas,
        "template": template
    }

	return {
		'statusCode': 200
		'body': json.dumps(response)
	}


def create-user(event):
	userId = event["queryStringParameters"]['deviceId'] + "-" + str(time.time_ns())
    baseline = { "flow":10, "volume":20 }
    create_user(userId, baseline, int(time.time()) )

    return {
        'statusCode': 200,
        'body': json.dumps(userId)
    }


def get-drawing(event):
	drawingId = event["queryStringParameters"]['drawingId']
	userId = img['drawingId'].split('-')[0]

	response = {
		"png": s3_lib.getfile('artsy-bucket', f'drawings/{userId}/{drawingId}.png'),
		"svg": s3_lib.getfile('artsy-bucket', f'drawings/{userId}/{drawingId}.svg')
	}

	return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


def get_templates(event):
    templates = {str(n).zfill(2):s3_lib.getfile('artsy-bucket', f'backgrounds/png/{str(n).zfill(2)}.png') for n in range(1, 27) }
    return {
        'statusCode': 200,
        'body': json.dumps(templates)
    }


def create-drawing(event):
	create_drawing(event['userId'],create_id(event['userId']),event['template'],time.time_ns())
    return {
        'statusCode': 200,
        'body': str(type(drawingIds))
    }

def save-drawing(event):
	response = s3_lib('artsy-bucket',event['drawingId'])
    set_title(event['drawingId'],event['title'])
    return {
        'statusCode': 200,
        'body': json.dumps(response),
        'png':str(event['drawingId'])+".png",
        'svg': str(event['drawingId'])+".svg"
    }


def purchase-brush(event):
    userId = event['headers']['userId']
    brushId = event['headers']['brushId']
    cost = event['headers']['cost']
    add_coins(userId, cost*(-1))
    add_brush(userId, brushId)
    return {
        'statusCode': 200,
    }


def purchase-paint(event):
	userId = event['headers']['paintId']
    paintId = event['headers']['paintId']
    cost = event['headers']['cost']
    add_coins(userId, cost*(-1))
    add_paint(userId, paintId)
    return {
        'statusCode': 200,
    }


def purchase-background(event):
	userId = event['headers']['userId']
    backgroundId = event['headers']['backgroundId']
    cost = event['headers']['cost']
    add_coins(userId, cost*(-1))
    add_background(userId, backgroundId)
    return {
        'statusCode': 200,
    }

def get-gallery(event):
	canvases = fetch_gallery_canvases()
    canvases = sorted(canvases, key = lambda i: i['modified'],reverse=True)
    canvases = map(image_object, canvases)
    templates = fetch_gallery_coloringPages()
    templates = sorted(templates, key = lambda i: i['modified'],reverse=True)
    templates = map(image_object, templates)
    response = {
        "canvases": canvases,
        "templates": templates
    }
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


def publish-to-gallery(event):
	drawingId = event['headers']['drawingId']
    title = event['headers']['title']
    set_title(drawingId, title)
    publish_drawing(drawingId)
    return {
        'statusCode': 200
    }

def add-breath(event):
    currTime = time.time_ns()
    breath = [currTime,event['flow'],event['volume']]
    add_raw_breath(event['userId'],breath)
	score = compute_score(event['flow'],event['volume'])
    baseline = get_user_attr(event['userId'], ["baseline"])['baseline']
    LOWBAR = 0.4
    #LOWBAR = 0 #TEST VALUE
    UNLIMITED_DURATION = 3600000000000 #one hour in nanoseconds
    #UNLIMITED_DURATION = 10000000000 #10 seconds in nanoseconds | TEST VALUE
    
    if(score > LOWBAR*baseline):
        if(get_user_attr(event['userId'],['unlimitedExpiration'])['unlimitedExpiration']<currTime):
            add_breath(event['userId'])
            if(get_user_attr(event['userId'],['breathCount'])['breathCount']==10):
                set_unlimited(event['userId'], currTime+UNLIMITED_DURATION)
        add_coins(event['userId'],score)
    if(score > baseline):
        set_baseline(event['userId'],score)
    
    return {
        'statusCode': 200,
        'seconds until use': (get_user_attr(event['userId'],['unlimitedExpiration'])['unlimitedExpiration']-time.time_ns())/1000000000,
        'balance': get_user_attr(event['userId'],['coins'])['coins'],
        'breathCount': get_user_attr(event['userId'],['breathCount'])['breathCount']
    }


#Helper functions
def create_id(userId):
    return str(userId) + '-' + str(time.time_ns())

def image_object(img):
    userId = img['drawingId'].split('-')[0]
    return {
        "imageUrl": s3_lib.getfile('artsy-bucket', f'drawings/{userId}/{img['drawingId']}.png')
        "title": img['title']
    }

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

apiDict = {
	"get-user-info": get-user-info,
	"get-user-art": get-user-art,
	"create-user": create-user,
	"get-drawing": get-drawing,
	"get-templates": get-templates,
	"create-drawing": create-drawing,
	"save-drawing": save-drawing,
	"purchase-brush": purchase-brush,
	"purchase-paint": purchase-paint,
	"purchase-background": purchase-background,
	"get-gallery": get-gallery,
	"publish-to-gallery": publish-to-gallery,
	"add-breath": add-breath
}
