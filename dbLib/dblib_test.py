 from dblib import *
#from mockLib import *
import time
import pprint
import json

#time = time.time() # time when using real library
# time = 0 # time when using mock

#tests = {
#    'user_tests': [
#        {
#            'name': "create_user and get_user_attr",
#            'description': 'Create User and fetch default state of the user: tests create_user and get_user_attr when key exists',
#            'user_id': '1',
#            'functions': [create_user],
#            'args': [('1', {'flow': 10,'volume': 20}, time)],
#            'expected': {
#                'user_id': '1',
#                'coins': 0,
#                'brushes': [],
#                'paints': [],
#                'baseline': {
#                    'flow': 10,
#                    'volume': 20
#                },
#                'history': [],
#                'backgrounds': [],
#                'drawings': [],
#                'lastBreath': time
#            }
#        }
#    ],
#    'drawing_tests':
#}

function_map = {
    "create_user": create_user,
    "get_user_attr": get_user_attr,
    "add_coins": add_coins,
    "add_brush": add_brush,
    "add_paint": add_paint,
    "add_background": add_background,
    "set_baseline": set_baseline,
    "add_breath": add_breath,
    "create_drawing": create_drawing,
    "get_drawing_attr": get_drawing_attr,
    "publish_drawing": publish_drawing,
    "unpublish_drawing": unpublish_drawing,
    "add_like": add_like,
    "fetch_gallery": fetch_gallery,
    "fetch_user_art": fetch_user_art
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

def report(passed, test, result):
    output = f'TEST::{test["name"]}{"."*25}{GREEN("PASS") if passed else RED("FAIL")}'
    if passed:
        print(output)
    else:
        actual, expected = compare(result, test['expected'])
        output += f'\n{YELLOW("Description:")} {test["description"]}\n\n{RED("EXPECTED:")}\n{expected}\n\n{RED("ACTUAL:")}\n{actual}\n{YELLOW("*"*60)}\n\n'
        print(output)

def check_result(test):
    attrs = ['user_id', 'baseline', 'coins', 'history', 'brushes', 'paints', 'backgrounds', 'drawings', 'lastBreath']
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
    elif result == test['expected']:
        report(True, test, result)
        return True
    else:
        report(False, test, result)
        return False

def execute_user_test(test):
    results = [0, 0]
    calls = test['functions']
    args = test['args']
    for i in range(len(calls)):
        func = function_map[calls[i]]
        func(*args[i])
        result = check_result(test)
        if result:
            results[0] += 1
        else:
            results[1] += 1
    print(f'\n\nRESULTS: {sum(results)} total tests executed\n\t{GREEN(str(results[0]) + " PASSED")}\n\t{RED(str(results[1]) + " FAILED")}')

def test(tests):
    for test in tests['user_tests']:
        execute_user_test(test)
        
def main():
    tests = json.load('dbLib_tests.json')
    test(tests)

if __name__ == "__main__":
    main()

