import json

def error_code(code, message):
    error={}
    error['code'] = code
    error['message'] = message
    return json.dumps(error, indent=4)
