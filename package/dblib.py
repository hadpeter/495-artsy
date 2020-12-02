import math
import boto3
import botocore
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

user_table = dynamodb.Table('users')
drawing_table = dynamodb.Table('drawings')
id_table = dynamodb.Table('ids')

class DatabaseException(Exception):
    """Exception raised for errors in database library.
    Attributes:
        function -- function error occured in
        message -- explanation of the error
    """

    def __init__(self, function, message="error in database library"):
        self.function = function
        self.message = message
        super().__init__(self.message)


##########################################################
############                              ################
############       User Table Library     ################
############                              ################
##########################################################


def create_user(deviceId, userId):
    # update user table
    try:
        user_table.put_item(
            Item = {
                'userId': userId,
                'coins': 0,
                'brushes': [],
                'paints': [],
                'baseline': 0,
                'breathCount': 0,
                'backgrounds': [],
                'drawings': [],
                'breathHistory': [],
                'unlimitedExpiration': 0
            },
            ConditionExpression=Attr('userId').not_exists()
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
        raise DatabaseException("create_user", "userId already exists")
    # update ids table
    try:
        id_table.update_item(
            Key = {
                'deviceId': deviceId
            },
            UpdateExpression='UPDATE userId :c',
            ExpressionAttributeValues={ ":c": userId }
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
        raise DatabaseException("create_user", "deviceId unable to update")

def get_user_id(deviceId):
    response = id_table.get_item(
        Key={'deviceId': deviceId}
    )
    if ('Item' in response.keys()):
        return response['Item']
    else:
        raise DatabaseException("get_user_id", "deviceId does not exist")

def get_user_attr(userId, attrs):
    projection = ', '.join(attrs)
    response = user_table.get_item(
        Key={'userId': userId},
        ProjectionExpression=projection
    )
    if ('Item' in response.keys()):
        return response['Item']
    else:
        raise DatabaseException("get_user_attr", "userId does not exist")
    
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
        raise DatabaseException("add_coins", "userId does not exist")
    
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
        raise DatabaseException("add_brush", "userId does not exist")
    
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
        raise DatabaseException("add_paints", "userId does not exist")

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
        raise DatabaseException("add_background", "userId does not exist")

def add_raw_breath(userId, breath):
    try:
        user_table.update_item(
            Key={
                'userId': userId
            },
            UpdateExpression='SET breathHistory = list_append(breathHistory, :b)',
            ConditionExpression=Attr('userId').eq(userId),
            ExpressionAttributeValues={ ":b": [breath] }
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
        raise DatabaseException("add_brush", "userId does not exist")
        
def set_baseline(userId, val):
    try:
        user_table.update_item(
            Key={
                'userId': userId
            },
            UpdateExpression='SET baseline = :b',
            ConditionExpression=Attr('userId').eq(userId),
            ExpressionAttributeValues={ ":b": val }
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
        raise DatabaseException("set_baseline", "userId does not exist")
        
def add_breath(userId):
    try:
        count = user_table.get_item(
            Key={'userId': userId},
            ProjectionExpression='breathCount'
        )['Item']['breathCount']
        user_table.update_item(
            Key={
                'userId': userId
            },
            UpdateExpression='SET breathCount = :b',
            ConditionExpression=Attr('userId').eq(userId),
            ExpressionAttributeValues={ ":b": count%10+1 }
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
        raise DatabaseException("add_breath", "userId does not exist")
        
def set_unlimited(userId, time):
    try:
        user_table.update_item(
            Key={
                'userId': userId
            },
            UpdateExpression='SET unlimitedExpiration = :b',
            ConditionExpression=Attr('userId').eq(userId),
            ExpressionAttributeValues={ ":b": time }
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
        raise DatabaseException("set_unlimited", "userId does not exist")
    
    
    
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
        raise DatabaseException("create_drawing", "drawingId already exists")
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
        raise DatabaseException("create_drawing", "userId does not exist")
            
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
        raise DatabaseException("get_drawing_attr", "drawingId does not exist")

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
        raise DatabaseException("publish_drawing", "drawingId does not exist")
        
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
        raise DatabaseException("set_title", "drawingId does not exist")
        
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
        raise DatabaseException("update_modified", "drawingId does not exist")
        
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
        raise DatabaseException("unpublish_drawing", "drawingId does not exist")
        
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
        raise DatabaseException("add_like", "drawingId does not exist")
        
def fetch_gallery_all():
    response = drawing_table.scan(
        ProjectionExpression='drawingId, title, coloringPage, modified',
        FilterExpression=Attr('published').eq(True)
    )
    if ('Items' in response.keys()):
        return response['Items']
    else:
        return []
        
def fetch_gallery_coloringPages():
    response = drawing_table.scan(
        ProjectionExpression='drawingId, title, coloringPage, modified',
        FilterExpression=Attr('published').eq(True) & Attr('coloringPage').ne('')
    )
    if ('Items' in response.keys()):
        return response['Items']
    else:
        return []
        
def fetch_gallery_canvases():
    response = drawing_table.scan(
        ProjectionExpression='drawingId, title, modified',
        FilterExpression=Attr('published').eq(True) & Attr('coloringPage').eq('')
    )
    if ('Items' in response.keys()):
        return response['Items']
    else:
        return []

def fetch_user_art_all(userId):
    user = get_user_attr(userId, ['drawings'])
    drawings = user['drawings']
    if len(drawings) == 0:
        return []
    response = drawing_table.scan(
        ProjectionExpression='drawingId, title, coloringPage, modified',
        FilterExpression=Attr('drawingId').is_in(drawings)
    )
    if ('Items' in response.keys()):
        return response['Items']
    else:
        raise DatabaseException("fetch_user_art_all", "userId does not exist")
        
def fetch_user_art_coloringPages(userId):
    user = get_user_attr(userId, ['drawings'])
    drawings = user['drawings']
    if len(drawings) == 0:
        return []
    response = drawing_table.scan(
        ProjectionExpression='drawingId, title, coloringPage, modified',
        FilterExpression=Attr('drawingId').is_in(drawings) & Attr('coloringPage').ne('')
    )
    if ('Items' in response.keys()):
        return response['Items']
    else:
        raise DatabaseException("fetch_user_art_coloringPages", "userId does not exist")
        
def fetch_user_art_canvases(userId):
    user = get_user_attr(userId, ['drawings'])
    drawings = user['drawings']
    if len(drawings) == 0:
        return []
    response = drawing_table.scan(
        ProjectionExpression='drawingId, title, modified',
        FilterExpression=Attr('drawingId').is_in(drawings) & Attr('coloringPage').eq('')
    )
    if ('Items' in response.keys()):
        return response['Items']
    else:
        raise DatabaseException("fetch_user_art_canvases", "userId does not exist")

def add_drawing_tag(drawingId, tag):


def get_drawing_tags(drawingID):
 