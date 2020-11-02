import boto3
import botocore
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

user_table = dynamodb.Table('users')
drawing_table = dynamodb.Table('drawings')


##########################################################
############                              ################
############       User Table Library     ################
############                              ################
##########################################################


def create_user(userId, time):
    try:
        user_table.put_item(
            Item = {
                'userId': userId,
                'coins': 0,
                'brushes': [],
                'paints': [],
                'baseline': {'flow': None, 'volume': None},
                'history': [],
                'backgrounds': [],
                'drawings': [],
                'lastBreath': time
            },
            ConditionExpression=Attr('userId').not_exists()
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise

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
    try:
        user_table.update_item(
            Key={
                'userId': userId
            },
            UpdateExpression='ADD coins :c',
            ConditionExpression=Attr('userId').eq(userId),
            ExpressionAttributeValues={ ":c": coins }
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
    
def add_brush(userId, brushId):
    try:
        user_table.update_item(
            Key={
                'userId': userId
            },
            UpdateExpression='SET brushes = list_append(brushes, :b)',
            ConditionExpression=Attr('userId').eq(userId),
            ExpressionAttributeValues={ ":b": [brushId] }
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
    
def add_paint(userId, paintId):
    try:
        user_table.update_item(
            Key={
                'userId': userId
            },
            UpdateExpression='SET paints = list_append(paints, :p)',
            ConditionExpression=Attr('userId').eq(userId),
            ExpressionAttributeValues={ ":p": [paintId] }
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
    
def add_background(userId, backgroundId):
    try:
        user_table.update_item(
            Key={
                'userId': userId
            },
            UpdateExpression='SET backgrounds = list_append(backgrounds, :b)',
            ConditionExpression=Attr('userId').eq(userId),
            ExpressionAttributeValues={ ":b": [backgroundId] }
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
    
def set_baseline(userId, flow, vol):
    baseline = {
        'flow': flow,
        'volume': vol
    }
    try:
        user_table.update_item(
            Key={
                'userId': userId
            },
            UpdateExpression='SET baseline = :b',
            ConditionExpression=Attr('userId').eq(userId),
            ExpressionAttributeValues={ ":b": baseline }
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
    
def add_breath(userId, flow, vol, time):
    breath = [{
        'flow': flow,
        'volume': vol
    }]
    try:
        user_table.update_item(
            Key={
                'userId': userId
            },
            UpdateExpression='SET history = list_append(history, :b), lastBreath = :t',
            ConditionExpression=Attr('userId').eq(userId),
            ExpressionAttributeValues={ ":b": breath, ":t": time }
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
    
    
    
##########################################################
############                              ################
############     Drawing Table Library    ################
############                              ################
##########################################################


def create_drawing(userId, drawingId, coloringPage, time):
    try:
        drawing_table.put_item(
            Item = {
                'drawingId': drawingId,
                'published': False,
                'modified': time,
                'coloringPage': coloringPage,
                'title': '',
                'likes': 0,
                'comments': []
            },
            ConditionExpression=Attr('drawingId').not_exists()
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
        return
    try:
        user_table.update_item(
            Key={
                'userId': userId
            },
            UpdateExpression='SET drawings = list_append(drawings, :d)',
            ConditionExpression=Attr('userId').eq(userId),
            ExpressionAttributeValues={ ":d": [drawingId] }
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
        delete_drawing(drawingId)
            
def delete_drawing(drawingId):
    drawing_table.delete_item(
        Key={
        'drawingId': drawingId
        }
    )

def get_drawing_attr(drawingId, attrs):
    projection = ', '.join(attrs)
    response = drawing_table.get_item(
        Key={'drawingId': drawingId},
        ProjectionExpression=projection
    )
    if ('Item' in response.keys()):
        return response['Item']
    else:
        return None

def publish_drawing(drawingId):
    try:
        drawing_table.update_item(
            Key={
                'drawingId': drawingId
            },
            UpdateExpression='SET published = :b',
            ConditionExpression=Attr('drawingId').eq(drawingId),
            ExpressionAttributeValues={ ":b": True }
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
            
def set_title(drawingId, title):
    try:
        drawing_table.update_item(
            Key={
                'drawingId': drawingId
            },
            UpdateExpression='SET title = :b',
            ConditionExpression=Attr('drawingId').eq(drawingId),
            ExpressionAttributeValues={ ":b": title }
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
            
def update_modified(drawingId, time):
    try:
        drawing_table.update_item(
            Key={
                'drawingId': drawingId
            },
            UpdateExpression='SET modified = :b',
            ConditionExpression=Attr('drawingId').eq(drawingId),
            ExpressionAttributeValues={ ":b": time }
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
    
def unpublish_drawing(drawingId):
    try:
        drawing_table.update_item(
            Key={
                'drawingId': drawingId
            },
            UpdateExpression='SET published = :b',
            ConditionExpression=Attr('drawingId').eq(drawingId),
            ExpressionAttributeValues={ ":b": False }
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
    
def add_like(drawingId):
    try:
        drawing_table.update_item(
            Key={
                'drawingId': drawingId
            },
            UpdateExpression='ADD likes :one',
            ConditionExpression=Attr('drawingId').eq(drawingId),
            ExpressionAttributeValues={ ":one": 1 }
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise

def fetch_gallery_all():
    response = drawing_table.scan(
        ProjectionExpression='drawingId, title, coloringPage, modified',
        FilterExpression=Attr('published').eq(":t"),
        ExpressionAttributeValues={ ":b": True }
    )
    if ('Items' in response.keys()):
        return response['Items']
    else:
        return None
        
def fetch_gallery_coloringPages():
    response = drawing_table.scan(
        ProjectionExpression='drawingId, title, coloringPage, modified',
        FilterExpression=Attr('published').eq(":t") & Attr('coloringPage').ne(":t"),
        ExpressionAttributeValues={ ":b": True, ":t": '' }
    )
    if ('Items' in response.keys()):
        return response['Items']
    else:
        return None
        
def fetch_gallery_canvases():
    response = drawing_table.scan(
        ProjectionExpression='drawingId, title, modified',
        FilterExpression=Attr('published').eq(":t") & Attr('coloringPage').eq(":t"),
        ExpressionAttributeValues={ ":b": True, ":t": '' }
    )
    if ('Items' in response.keys()):
        return response['Items']
    else:
        return None

def fetch_user_art_all(userId):
    user = get_user_attr(userId, ['drawings'])
    drawings = user['drawings']
    response = drawing_table.query(
        ProjectionExpression='drawingId, title, coloringPage, modified',
        KeyConditionExpression=Attr('drawingId').is_in(":lst"),
        ExpressionAttributeValues={ ":lst": drawings }
    )
    if ('Items' in response.keys()):
        return response['Items']
    else:
        return None
        
def fetch_user_art_coloringPages(userId):
    user = get_user_attr(userId, ['drawings'])
    drawings = user['drawings']
    response = drawing_table.query(
        ProjectionExpression='drawingId, title, coloringPage, modified',
        KeyConditionExpression=Attr('drawingId').is_in(":lst") & Attr('coloringPage').ne(":t"),
        ExpressionAttributeValues={ ":lst": drawings, ":t": '' }
    )
    if ('Items' in response.keys()):
        return response['Items']
    else:
        return None
        
def fetch_user_art_canvases(userId):
    user = get_user_attr(userId, ['drawings'])
    drawings = user['drawings']
    response = drawing_table.query(
        ProjectionExpression='drawingId, title, modified',
        KeyConditionExpression=Attr('drawingId').is_in(":lst") & Attr('coloringPage').eq(":t"),
        ExpressionAttributeValues={ ":lst": drawings, ":t": '' }
    )
    if ('Items' in response.keys()):
        return response['Items']
    else:
        return None
    
