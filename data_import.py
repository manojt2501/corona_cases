import pyodbc
import logging
def create_conn(sql):
    logging.info('Connection getting initiated')
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + sql['server'] + ';DATABASE=' + sql['database'] + ';UID=' + sql['username'] + ';PWD=' + sql['password'])
    except pyodbc.Error:
        conn = False
    if conn:
        logging.info('connection created successfully with SQL')
        conn.close()
        return 1
    else:
        logging.error('Unable to create connection with SQL. please check connection string')
        conn.close()
        return 0

def table_import(sql,data):
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + sql['server'] + ';DATABASE=' + sql['database'] + ';UID=' + sql['username'] + ';PWD=' + sql['password'])
    except pyodbc.Error:
        conn = False
    logging.info('inside table import function')
    cursor= conn.cursor()
    for list in data:
        values = ', '.join("'" + str(x) + "'" for x in list.values())
        enc = values.encode("utf-8")
        sql = "INSERT INTO corona..daily_updates (country_name, country_code, new_cases, total_cases, new_deaths, total_deaths, new_recovered, total_recovered, date) VALUES (%s);" % (
            enc.decode().replace("d'I", "d''I"))
        # print(sql)
        # cursor.execute(sql)
        # cursor.commit()
    conn.close()

def last_updatecomp(sql):
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + sql['server'] + ';DATABASE=' + sql['database'] + ';UID=' + sql['username'] + ';PWD=' + sql['password'])
    except pyodbc.Error:
        conn = False
    cursor = conn.cursor()
    cursor.execute('select * from corona.. last_updated')
    last_updatetemp = cursor.fetchone()
    last_update=str(last_updatetemp).replace("('","").replace("', )","")
    print(last_update)
    return last_update









