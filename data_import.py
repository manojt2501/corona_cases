import pyodbc
import logging
def create_conn(sql,api_data):
    logging.info('Connection getting initiated')
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + sql['server'] + ';DATABASE=' + sql['database'] + ';UID=' + sql['username'] + ';PWD=' + sql['password'])
    except pyodbc.Error:
        conn = False
    if conn:
        logging.info('connection created successfully with SQL')
        logging.info('Calling table import function')
        table_import(conn,api_data)
    else:
        conn.close()
        logging.error('Unable to create connection with SQL. please check connection string')

def table_import(cnxn,data):
    logging.info('inside table import function')
    cursor= cnxn.cursor()
    for list in data:
        values = ', '.join("'" + str(x) + "'" for x in list.values())
        enc = values.encode("utf-8")
        sql = "INSERT INTO corona..daily_updates (country_name, country_code, new_cases, total_cases, new_deaths, total_deaths, new_recovered, total_recovered, date) VALUES (%s);" % (
            enc.decode().replace("d'I", "d''I"))
        # print(sql)
        # cursor.execute(sql)
        # cursor.commit()
    cnxn.close()







