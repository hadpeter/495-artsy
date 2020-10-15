import boto3
import time

client = boto3.client('dynamodb')

user_table = client.Table('users')
drawing_table = client.Table('drawings')


##########################################################
############                              ################
############       User Table Library     ################
############                              ################
##########################################################


def create_user(userId, baseline, time):
    user_table.put_item(
        Item = {
            'userId': userId,
            'coins': 0,
            'brushes': [],
            'paints': [],
            'baseline': baseline,
            'history': [],
            'backgrounds': [],
            'drawings': [],
            'lastBreath': time
        }
    )

def get_user_attr(userId, attrs):
    projection = ', '.join(attrs)
    response = user_table.get_item(
        Key={'userId': userId},
        ProjectionExpression=projection
    )
    if ('Item' in response.keys()):
        return response['Item']
    else:
        return None
    
    
def add_coins(userId, coins):
    user_table.update_item(
        Key={
            'userId': userId
        },
        UpdateExpression='ADD coins :c',
        ConditionExpression=Attr('userId').eq(userId),
        ExpressionAttributeValues={ ":c": coins }
    )
    
def add_brush(userId, brushId):
    user_table.update_item(
        Key={
            'userId': userId
        },
        UpdateExpression='ADD brushes :c',
        ConditionExpression=Attr('userId').eq(userId),
        ExpressionAttributeValues={ ":b": [brushId] }
    )
    
def add_paint(userId, paintId):
    user_table.update_item(
        Key={
            'userId': userId
        },
        UpdateExpression='ADD paints :p',
        ConditionExpression=Attr('userId').eq(userId),
        ExpressionAttributeValues={ ":p": [paintId] }
    )
    
def add_background(userId, backgroundId):
    user_table.update_item(
        Key={
            'userId': userId
        },
        UpdateExpression='ADD backgrounds :b',
        ConditionExpression=Attr('userId').eq(userId),
        ExpressionAttributeValues={ ":b": [backgroundId] }
    )
    
def set_baseline(userId, flow, vol):
    baseline = {
        'flow': flow,
        'volume': volume
    }
    user_table.update_item(
        Key={
            'userId': userId
        },
        UpdateExpression='SET baseline = :b',
        ConditionExpression=Attr('userId').eq(userId),
        ExpressionAttributeValues={ ":b": baseline }
    )
    
def add_breath(userId, flow, vol, time):
    breath = {
        'flow': flow,
        'volume': volume
    }
    user_table.update_item(
        Key={
            'userId': userId
        },
        UpdateExpression='SET history = list_append(history, :b), lastBreath = :t',
        ConditionExpression=Attr('userId').eq(userId),
        ExpressionAttributeValues={ ":b": breath, ":t": time }
    )
    
    
    
##########################################################
############                              ################
############     Drawing Table Library    ################
############                              ################
##########################################################


def create_drawing(userId, drawingId, coloringPage, title, file):
    drawing_table.put_item(
        Item = {
            'drawingId': drawingId,
            'published': False,
            'modified': time.time(),
            'coloringPage': coloringPage,
            'title': title,
            'likes': 0,
            'comments': [],
            'data' : file
        }
    )
    user_table.update_item(
        Key={
            'userId': userId
        },
        UpdateExpression='ADD drawings :d',
        ConditionExpression=Attr('userId').eq(userId),
        ExpressionAttributeValues={ ":d": [drawingId] }
    )

def get_drawing_attr(drawingId, attrs):
    projection = ', '.join(attrs)
    response = user_table.get_item(
        Key={'drawingId': drawingId},
        ProjectionExpression=projection
    )
    return response['Item']

def publish_drawing(drawingId):
    drawing_table.update_item(
        Key={
            'drawingId': drawingId
        },
        UpdateExpression='SET published = :b',
        ConditionExpression=Attr('drawingId').eq(drawingId),
        ExpressionAttributeValues={ ":b": True }
    )
    
def unpublish_drawing(drawingId):
    drawing_table.update_item(
        Key={
            'drawingId': drawingId
        },
        UpdateExpression='SET published = :b',
        ConditionExpression=Attr('drawingId').eq(drawingId),
        ExpressionAttributeValues={ ":b": False }
    )
    
def add_like(drawingId):
    drawing_table.update_item(
        Key={
            'drawingId': drawingId
        },
        UpdateExpression='ADD likes :one',
        ConditionExpression=Attr('drawingId').eq(drawingId),
        ExpressionAttributeValues={ ":one": 1 }
    )

def fetch_gallery():
    drawing_table.scan(
        ProjectionExpression='drawingId, title, data',
        FilterExpression=Attr(published).eq(":t"),
        ExpressionAttributeValues={ ":b": True }
    )

def fetch_user_art(userId):
    user = get_user_attr(userId, ['drawings']):
    drawings = user['drawings']
    drawing_table.query(
        ProjectionExpression='drawingId, title, data',
        KeyConditionExpression=Attr(published).is_in(":lst"),
        ExpressionAttributeValues={ ":lst": drawings }
    )

    
