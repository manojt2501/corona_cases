import pyodbc
import logging
def create_conn():
    server = 'localhost\sql,1433'
    database = 'master'
    username = 'sa22'
    password = 'Fiduciary@123'
    logging.info('Connection getting initiated')
    try:
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    except pyodbc.Error:
        cnxn = False
    if cnxn:
        logging.info('connection created successfully with SQL')
    else:
        logging.error('Unable to create connection with SQL. please check connection param')

