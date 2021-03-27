import request_api
import data_master
import sql_queries
from flask import render_template, Flask, request, redirect, url_for
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', filename='process.log')
app = Flask(__name__)


@app.route('/data_import')
def main():
    sql_string = data_master.data_config('sql')
    url = data_master.data_config('url')
    if request_api.check_valid(url) == 'success':
        logging.info('API sent valid response, proceeding to verify SQL connection')
        if sql_queries.check_conn(sql_string) == 'success':
            logging.info('SQL connection established, proceeding with data comparison')
            corona = request_api.get_content(url)
            if data_master.date_compare(corona) != sql_queries.last_update_comp(sql_string):
                logging.info('data comparison completed, proceeding to import data')
                daily_updates = data_master.daily_cases(corona)
                return sql_queries.table_import(sql_string, daily_updates)
            else:
                logging.info(f"Data already present for date '{data_master.date_compare(corona)}'.Data import skipped")
                return 'failed. Please verify log for more info'
        else:
            logging.error('SQL failed to connect. Unable to proceed further')
            return 'failed. Please verify log for more info'
    else:
        logging.error('API response failed. Unable to proceed further')
        return 'failed. Please verify log for more info'


@app.route('/runSQL', methods=["POST", "GET"])
def runsql():
    if request.method == 'POST':
        query = request.form["nm"]
        return redirect(url_for('show_result', qry=query))
    else:
        return render_template('run_sql.html')


@app.route('/show_result/<qry>')
def show_result(qry):
    query_input = qry.split()
    query_not_allowed = ['delete', 'update', 'insert', 'alter', 'drop', 'truncate', 'create']
    if data_master.query_check(query_input, query_not_allowed) is not True:
        sql = data_master.data_config('sql')
        if sql_queries.check_conn(sql) == 'success':
            cursor = sql_queries.create_conn(sql)
            cursor.execute(qry)
            headers = [i[0] for i in cursor.description]
            fetch_data = cursor.fetchall()
            cursor.close()
            return render_template('show_result.html', head=headers, data=fetch_data)
        else:
            return 'failed. Please verify log for more info'

    else:
        logging.error('query other than select statement are performed')
        return 'Query can be performed only with SELECT keyword'


if __name__ == '__main__':
    app.run(host='localhost', port=8000)
