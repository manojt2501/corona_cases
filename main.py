import request_api
import data_master
import sql_queries
import error_handler
from flask import Flask, request
import logging
import json
import datetime
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', filename='process.log')
app = Flask(__name__)


@app.route('/data_import', methods=["POST"])
def main():
    sql_string = data_master.data_config('sql')
    url = data_master.data_config('url')
    data = request.get_json()
    user_name = data.get('u_name', '')
    password = data.get('pwd', '')
    if request_api.check_valid(url) is True:
        logging.info('API sent valid response, proceeding to verify SQL connection')
        if sql_queries.check_conn(sql_string) is True:
            logging.info('SQL connection established, proceeding with data comparison')
            corona = request_api.get_content(url)
            if sql_queries.authentication(sql_string, user_name, password) == 'admin':
                if data_master.date_compare(corona) != sql_queries.last_update_comp(sql_string):
                    logging.info('data comparison completed, proceeding to import data')
                    daily_updates = data_master.daily_cases(corona)
                    return sql_queries.table_import(sql_string, daily_updates)
                else:
                    logging.info(f"Data already present for date '{data_master.date_compare(corona)}'")
                return error_handler.error_code('I-10', 'Data already imported')
            elif sql_queries.authentication(sql_string, user_name, password) == 'user':
                return error_handler.error_code('I-20', 'Only admin can import data')
            else:
                return error_handler.error_code('E-20', 'Invalid credentials or user not available')
        else:
            logging.error('SQL failed to connect. Unable to proceed further')
            return error_handler.error_code('E-10', 'SQL related problem occurred. Unable to process request')
    else:
        logging.error('API response failed. Unable to proceed further')
        return error_handler.error_code('E-0', 'failed to Fetch API response')


@app.route('/runSQL', methods=["GET"])
def sql():
    sql_string = data_master.data_config('sql')
    data = request.get_json()
    query = data.get('qry', '')
    user_name = data.get('u_name', '')
    password = data.get('pwd', '')
    if sql_queries.check_conn(sql_string) is True:
        if sql_queries.authentication(sql_string, user_name, password) == 'admin':
            query_input = query.split()
            query_not_allowed = ['delete', 'update', 'insert', 'alter', 'drop', 'truncate', 'create']
            if data_master.query_check(query_input, query_not_allowed) is not True:
                cursor = sql_queries.create_conn(sql_string)
                cursor.execute(query)
                headers = [i[0] for i in cursor.description]
                fetch_data = cursor.fetchall()
                cursor.close()
                json_data = []
                for result in fetch_data:
                    json_data.append(dict(zip(headers, result)))
                final1 = json.dumps(json_data, ensure_ascii=False, default=my_converter, indent=4)
                return final1.encode('UTF-8')
            else:
                return error_handler.error_code('I-0', 'Query statement not allowed')
        else:
            return error_handler.error_code('E-20', 'Invalid credentials or user not available')
    else:
        return error_handler.error_code('E-10', 'SQL related problem occurred. Unable to process request')


def my_converter(o):
    if isinstance(o, datetime.date):
        return o.__str__()
    elif isinstance(o, bytes):
        return o.__str__().replace("b'", "").replace("'", "").replace("\\", "")


if __name__ == '__main__':
    app.run(host='localhost', port=8000)
