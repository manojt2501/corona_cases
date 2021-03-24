import request
import configparser
import content_data
import data_import
from flask import render_template
import logging
from flask import Flask

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', filename='process.log')
app = Flask(__name__)
@app.route('/data_import')
def main():
    logging.info('processing your request')
    Config = configparser.ConfigParser()
    Config.read(r"D:\code\corona_cases\connection.ini")
    SQL_string = dict(Config.items('SQL'))
    URL = dict(Config.items('API'))
    if request.check_valid(URL) == 'success':
        logging.info('API sent valid response, proceeding to verify SQL connection')
        if data_import.check_conn(SQL_string) == 'success':
            logging.info('SQL connection established, proceeding with data comparison')
            corona = request.get_content(URL)
            if content_data.date_compare(corona) != data_import.last_updatecomp(SQL_string):
                logging.info('data comparison completed, proceeding to import data')
                daily_updates = content_data.daily_cases(corona)
                Result= data_import.table_import(SQL_string,daily_updates)
                return Result
            else:
                logging.info(f"Data already present for the same date '{content_data.date_compare(corona)}' in table. Hence data import skipped")
                return 'failed. Please verify log for more info'
        else:
            logging.error('SQL failed to connect. Unable to proceed further')
            return 'failed. Please verify log for more info'
    else:
        logging.error('API response failed. Unable to proceed further')
        return 'failed. Please verify log for more info'

@app.route('/show_data')
def show_data():
    Config = configparser.ConfigParser()
    Config.read(r"D:\code\corona_cases\connection.ini")
    sql = dict(Config.items('SQL'))
    cursor = data_import.create_conn(sql)
    cursor.execute('select * from corona.. daily_updates')
    fetch_data = cursor.fetchall()
    cursor.close()
    return render_template('show_data.html', data=fetch_data)

if __name__=='__main__':
    app.run(host='localhost', port=8000)
    show_data()


