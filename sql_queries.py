import pyodbc
import logging
import error_handler


# check SQL connectivity
def create_conn(sql):
    logging.info('Initiating connection with SQL')
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + sql['server'] + ';DATABASE='
            + sql['database'] + ';UID=' +
            sql['username'] + ';PWD=' + sql['password'], timeout=1)
        cursor = conn.cursor()
        return cursor
    except pyodbc.Error as er:
        sql_error = er.args[1]
        logging.error(sql_error)
        return False


# to import daily data from API to table
def table_import(sql, data):
    cursor = create_conn(sql)
    logging.info('inside table import function')
    for items in data:
        values = ', '.join("'" + str(x).replace("'", "''") + "'" for x in items.values())
        enc = values.encode("utf-8")
        sql = "INSERT INTO corona..daily_updates " \
              "(country_name, country_code, new_cases, total_cases, new_deaths, " \
              "total_deaths, new_recovered, total_recovered, date) VALUES (%s);" \
              % (enc.decode())
        cursor.execute(sql)
        cursor.commit()
    cursor.close()
    return error_handler.error_code('I-20', 'Data imported successfully')


# function to fetch latest updated date
def last_update_comp(sql):
    cursor = create_conn(sql)
    cursor.execute('select * from corona.. last_updated')
    last_update_temp = cursor.fetchone()
    last_update = str(last_update_temp).replace("('", "").replace("', )", "")
    cursor.close()
    return last_update


def authentication(sql, u_name, pwd):
    cursor = create_conn(sql)
    cursor.execute(f"select access_type from corona.. logins where u_name='{u_name}' and pwd='{pwd}'")
    data = cursor.fetchone()
    date_last = str(data).replace("('", "").replace("', )", "")
    if data:
        if date_last == 'A':
            return 'admin'
        else:
            return 'user'
    else:
        return False
