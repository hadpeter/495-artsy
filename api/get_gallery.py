import json
from dblib import *
from s3_lib import get_file as signedURL

def image_object(img):
    userId = img['drawingId'].split('-')[0]
    return {
        "imageUrl": signedURL('artsy-bucket', f'drawings/{userId}/{img['drawingId']}.png')
        "title": img['title']
    }
    
def get_gallery(event, context):
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
