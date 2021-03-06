import request_api
import data_master
from sql_queries import DatabaseDriver
from marshmallow import Schema, fields, ValidationError
from flask import Flask, request
import logging
import json
import datetime
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', filename='process.log')
app = Flask(__name__)


class RequestValidate(Schema):
    u_name = fields.String(required=True)
    pwd = fields.String(required=True)
    conn_type = fields.String(required=True)


class ChildClass(RequestValidate):
    qry = fields.String(required=True)


@app.route('/data_import', methods=["POST"])
def main():
    url = data_master.data_config('API')
    data = request.get_json()
    try:
        RequestValidate().load(data)
        user_name = data.get('u_name', '')
        password = data.get('pwd', '')
        conn_type = data.get('conn_type', '')
        sql_string = 0
        if conn_type == 'local':
            sql_string = data_master.data_config('SQL_local')
        elif conn_type == 'AWS':
            sql_string = data_master.data_config('SQL_AWS')
        corona = request_api.get_content(url)
        if corona is not False:
            logging.info('API sent valid response, proceeding to verify SQL connection')
            db = DatabaseDriver(sql_string)
            if db.create_conn() is not False:
                logging.info('SQL connection established, proceeding with data comparison')
                if db.authentication(user_name, password) == 'admin':
                    if data_master.date_compare(corona) != db.last_update_comp():
                        logging.info('data comparison completed, proceeding to import data')
                        daily_updates = data_master.daily_cases(corona)
                        if db.table_import(daily_updates) is True:
                            db.close_conn()
                            return error_code('I-20', 'Data Imported successfully')
                        else:
                            db.close_conn()
                            return error_code('E-20', 'Data Imported Failed')
                    else:
                        logging.info(f"Data already present for date '{data_master.date_compare(corona)}'")
                        return error_code('I-10', 'Data already imported')
                elif db.authentication(user_name, password) == 'user':
                    return error_code('I-20', 'Only admin can import data')
                else:
                    return error_code('E-20', 'Invalid credentials or user not available')
            else:
                logging.error('SQL failed to connect. Unable to proceed further')
                return error_code('E-10', 'SQL related problem occurred. Unable to process request')
        else:
            logging.error('API response failed. Unable to proceed further')
            return error_code('E-0', 'failed to Fetch API response')
    except ValidationError as err:
        print(err.messages)
        return err.messages


@app.route('/runSQL', methods=["GET"])
def sql():
    data = request.get_json()
    try:
        ChildClass().load(data)
        query = data.get('qry', '')
        user_name = data.get('u_name', '')
        password = data.get('pwd', '')
        conn_type = data.get('conn_type', '')
        sql_string = 0
        if conn_type == 'local':
            sql_string = data_master.data_config('SQL_local')
        elif conn_type == 'AWS':
            sql_string = data_master.data_config('SQL_AWS')
        db = DatabaseDriver(sql_string)
        if db.create_conn() is not False:
            if db.authentication(user_name, password) == 'admin':
                query_input = query.split()
                query_not_allowed = ['delete', 'update', 'insert', 'alter', 'drop', 'truncate', 'create']
                if data_master.query_check(query_input, query_not_allowed) is not True:
                    fetch_data = db.execute(query)
                    result_data = fetch_data[1]
                    headers = fetch_data[0]
                    db.close_conn()
                    json_data = []
                    for result in result_data:
                        json_data.append(dict(zip(headers, result)))
                    final1 = json.dumps(json_data, ensure_ascii=False, default=my_converter, indent=4)
                    return final1.encode('UTF-8')
                else:
                    return error_code('I-0', 'Query statement not allowed')
            else:
                return error_code('E-20', 'Invalid credentials or user not available')
        else:
            return error_code('E-10', 'SQL related problem occurred. Unable to process request')
    except ValidationError as err:
        print(err.messages)
        return err.messages


def my_converter(o):
    if isinstance(o, datetime.date):
        return o.__str__()
    elif isinstance(o, bytes):
        return o.__str__().replace("b'", "").replace("'", "").replace("\\", "")


def error_code(code, message):
    error = {'code': code, 'message': message}
    return json.dumps(error, indent=4)


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=False)
