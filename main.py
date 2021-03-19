import request
import configparser
import content_data
import data_import
from flask import Flask
app = Flask(__name__)
@app.route('/get_data')
def main():
    Config = configparser.ConfigParser()
    Config.read(r"D:\code\corona_cases\connection.ini")
    SQL_string = dict(Config.items('SQL'))
    URL = dict(Config.items('API'))
    if request.check_valid(URL) != 0:
        corona = request.get_content(URL)
        daily_updates = content_data.daily_cases(corona)
        data_import.create_conn(SQL_string,daily_updates)
        return 'success'
    else:
        return 'failed'

if __name__=='__main__':
    app.run(host='localhost', port=8000, debug=True)


