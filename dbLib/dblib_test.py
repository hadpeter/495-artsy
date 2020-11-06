from dblib import *
import time
import pprint
import json
import decimal


function_map = {
    "create_user": create_user,
    "get_user_attr": get_user_attr,
    "add_coins": add_coins,
    "add_brush": add_brush,
    "add_paint": add_paint,
    "add_background": add_background,
    "set_baseline": set_baseline,
    "add_breath": add_breath,
    "set_unlimited": set_unlimited,
    "create_drawing": create_drawing,
    "delete_drawing": delete_drawing,
    "get_drawing_attr": get_drawing_attr,
    "publish_drawing": publish_drawing,
    "unpublish_drawing": unpublish_drawing,
    "add_like": add_like,
    "set_title": set_title,
    "update_modified": update_modified,
    "fetch_gallery_all": fetch_gallery_all,
    "fetch_gallery_coloringPages": fetch_gallery_coloringPages,
    "fetch_gallery_canvases": fetch_gallery_canvases,
    "fetch_user_art_all": fetch_user_art_all,
    "fetch_user_art_coloringPages": fetch_user_art_coloringPages,
    "fetch_user_art_canvases": fetch_user_art_canvases
}

def RED(x): 
    return("\033[91m {}\033[00m" .format(x)) 

def GREEN(x): 
    return("\033[92m {}\033[00m" .format(x))

def YELLOW(x): 
    return("\033[93m {}\033[00m" .format(x))

def compare(actual, expected):
    pp = pprint.PrettyPrinter(indent=2)
    return pp.pformat(expected), pp.pformat(actual)

def report(passed, test, result={}):
    output = f'TEST::{test["name"]}{"."*25}{GREEN("PASS") if passed else RED("FAIL")}'
    if passed:
        print(output)
    else:
        expected, actual = compare(result, test['expected'])
        output += f'\n{YELLOW("Description:")} {test["description"]}\n\n{RED("EXPECTED:")}\n{expected}\n\n{RED("ACTUAL:")}\n{actual}\n{YELLOW("*"*60)}\n\n'
        print(output)

def check_user_result(test):
    attrs = ['userId', 'baseline', 'coins', 'breathCount', 'brushes', 'paints', 'backgrounds', 'drawings', 'unlimitedExpiration']
    result = get_user_attr(test['user_id'], attrs)
    if result is None:
        if test['expected'] == "None":
            report(True, test, result)
            return True
        else:
            report(False, test, result)
            return False
    elif test['expected'] == "None":
        report(False, test, result)
        return False
    else:
        if result == test['expected']:
            report(True, test, result)
            return True
        else:
            report(False, test, result)
            return False
            
def check_drawing_result(test):
    attrs = ['drawingId', 'modified', 'filename', 'published', 'coloringPage', 'title', 'likes', 'comments']
    result = get_drawing_attr(test['drawing_id'], attrs)
    if result is None:
        if test['expected'] == "None":
            report(True, test, result)
            return True
        else:
            report(False, test, result)
            return False
    elif test['expected'] == "None":
        report(False, test, result)
        return False
    else:
        if result == test['expected']:
            report(True, test, result)
            return True
        else:
            report(False, test, result)
            return False
            
def check_gallery_result(result, test):
    if result is None:
        if test['expected'] == "None":
            report(True, test, result)
            return True
        else:
            report(False, test, result)
            return False
    elif test['expected'] == "None":
        report(False, test, result)
        return False
    else:
        if result == test['expected']:
            report(True, test, result)
            return True
        else:
            report(False, test, result)
            return False

def execute_user_test(test):
    calls = test['functions']
    args = test['args']
    for i in range(len(calls)):
        func = function_map[calls[i]]
        func(*args[i])
    result = check_user_result(test)
    return result
    
def execute_drawing_test(test):
    calls = test['functions']
    args = test['args']
    for i in range(len(calls)):
        func = function_map[calls[i]]
        func(*args[i])
    result = check_drawing_result(test)
    return result
    
def execute_gallery_test(test):
    calls = test['functions']
    args = test['args']
    response = None
    for i in range(len(calls)):
        func = function_map[calls[i]]
        response = func(*args[i])
    result = check_gallery_result(response, test)
    return result
    
def set_up_gallery_tests(tests):
    calls = tests['gallery_tests']['setup']['functions']
    args = tests['gallery_tests']['setup']['args']
    for i in range(len(calls)):
        func = function_map[calls[i]]
        func(*args[i])

def test(tests):
    results = [0, 0]
    for test in tests['user_tests']:
        try:
            result = execute_user_test(test)
        except DatabaseException as e:
            if test["expected"] != "None":
                raise e
            report(True, test)
        if result:
            results[0] += 1
        else:
            results[1] += 1
    for test in tests['drawing_tests']:
        try:
            result = execute_drawing_test(test)
        except DatabaseException as e:
            if test["expected"] != "None":
                raise e
            report(True, test)
        if result:
            results[0] += 1
        else:
            results[1] += 1
    set_up_gallery_tests(tests)
    for test in tests['gallery_tests']['tests']:
        try:
            result = execute_gallery_test(test)
        except DatabaseException as e:
            if test["expected"] != "None":
                raise e
            report(True, test)
        if result:
            results[0] += 1
        else:
            results[1] += 1
    print(f'\n\nRESULTS: {sum(results)} total tests executed\n\t{GREEN(str(results[0]) + " PASSED")}\n\t{RED(str(results[1]) + " FAILED")}')
    
def reset():
    dynamodb.Table('users').delete()
    dynamodb.Table('drawings').delete()
    table1 = dynamodb.create_table(
        TableName='users',
        KeySchema=[
            {
                'AttributeName': 'userId',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'userId',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table2 = dynamodb.create_table(
        TableName='drawings',
        KeySchema=[
            {
                'AttributeName': 'drawingId',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'drawingId',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait until the table exists.
    table1.meta.client.get_waiter('table_exists').wait(TableName='users')
    table2.meta.client.get_waiter('table_exists').wait(TableName='drawings')
        
def main():
    reset()
    with open('dbLib_tests.json') as f:
        tests = json.load(f)
        test(tests)

if __name__ == "__main__":
    main()

