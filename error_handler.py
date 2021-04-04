import json


def error_code(code, message):
    error = {'code': code, 'message': message}
    return json.dumps(error, indent=4)
