import request_api
import configparser
import data_master
import sql_queries
from flask import render_template
import logging
from flask import Flask
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', filename='process.log')
app = Flask(__name__)


@app.route('/data_import')
def main():
    logging.info('processing your request')
    config = configparser.ConfigParser()
    config.read(r"D:\code\corona_cases\connection.ini")
    sql_string = dict(config.items('SQL'))
    url = dict(config.items('API'))
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


@app.route('/show_data')
def show_data():
    config = configparser.ConfigParser()
    config.read(r"D:\code\corona_cases\connection.ini")
    sql = dict(config.items('SQL'))
    cursor = sql_queries.create_conn(sql)
    cursor.execute('select * from corona.. daily_updates')
    fetch_data = cursor.fetchall()
    cursor.close()
    return render_template('show_data.html', data=fetch_data)


if __name__ == '__main__':
    app.run(host='localhost', port=8000)
    show_data()
