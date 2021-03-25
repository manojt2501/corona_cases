import pyodbc
import logging


def check_conn(sql):
    logging.info('Connection getting initiated')
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + sql['server'] + ';DATABASE='
            + sql['database'] + ';UID=' +
            sql['username'] + ';PWD=' + sql['password'])
    except pyodbc.Error:
        conn = 0
    if conn:
        logging.info('connection created successfully with SQL')
        conn.close()
        return 'success'
    else:
        logging.error('Unable to create connection with SQL. please check connection string')
        return 'failed'


def create_conn(sql):
    conn1 = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + sql['server'] + ';DATABASE=' + sql['database'] + ';UID=' +
        sql['username'] + ';PWD=' + sql['password'])
    cursor = conn1.cursor()
    return cursor


def table_import(sql, data):
    cursor = create_conn(sql)
    logging.info('inside table import function')
    for items in data:
        values = ', '.join("'" + str(x).replace("'", "''") + "'" for x in items.values())
        enc = values.encode("utf-8")
        sql = "INSERT INTO corona..daily_updates (country_name, country_code, new_cases, total_cases, new_deaths, total_deaths, new_recovered, total_recovered, date) VALUES (%s);" \
              % (enc.decode())
        # print(sql)
        cursor.execute(sql)
        cursor.commit()
    cursor.close()
    return 'DATA imported successfully'


def last_update_comp(sql):
    cursor = create_conn(sql)
    cursor.execute('select * from corona.. last_updated')
    last_update_temp = cursor.fetchone()
    last_update = str(last_update_temp).replace("('", "").replace("', )", "")
    cursor.close()
    return last_update
