import pyodbc
import logging
import pymysql


class DatabaseDriver:
    def __init__(self, sql):
        self.conn = None
        self.cursor = None
        self.conn_type = sql['conn_type']
        if self.conn_type == 'local':
            self.server = sql['server']
            self.database = sql['database']
            self.userID = sql['username']
            self.pwd = sql['password']
        elif self.conn_type == 'AWS':
            self.host = sql['server']
            self.database = sql['database']
            self.userID = sql['username']
            self.pwd = sql['password']

    def create_conn(self):
        if self.conn_type == 'local':
            try:
                self.conn = pyodbc.connect(
                    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.server + ';DATABASE='
                    + self.database + ';UID=' +
                    self.userID + ';PWD=' + self.pwd, timeout=1)
                self.cursor = self.conn.cursor()
                return self.cursor
            except pyodbc.Error as er:
                sql_error = er.args[1]
                logging.error(sql_error)
                return False
        elif self.conn_type == 'AWS':
            try:
                self.conn = pymysql.connect(host=self.host, database=self.database, user=self.userID,
                                            password=self.pwd, port=3306, connect_timeout=1, autocommit=True)
                self.cursor = self.conn.cursor()
                return self.cursor
            except pymysql.Error as er:
                sql_error = er.args[1]
                logging.error(sql_error)
                return False

    def table_import(self, data):
        try:
            text = ''
            for items in data:
                start = '('
                values = start+', '.join("'" + str(x).replace("'", "''")+"'" for x in items.values())
                enc = values.encode("utf-8")
                text = text + (enc.decode()) + '),'
            sql_val = text.rstrip(text[-1])
            sql_key = "INSERT INTO corona. daily_updates (country_name, country_code, new_cases, total_cases, " \
                      "new_deaths, total_deaths, new_recovered, total_recovered, date) VALUES "
            execute_sql = sql_key + sql_val
            self.cursor.execute(execute_sql)
            return True
        except ImportError as error:
            logging.error(error)
            return False

    def last_update_comp(self):
        self.cursor.execute("select DATE_FORMAT(date,'%Y-%m-%d') as date from daily_updates order by 1 desc limit 1")
        last_update_temp = self.cursor.fetchone()
        last_update = last_update_temp[0]
        return last_update

    def authentication(self, u_name, pwd):
        self.cursor.execute(f"select access_type from corona. logins where u_name='{u_name}' and pwd='{pwd}'")
        data = self.cursor.fetchone()
        date_last = data[0][0]
        if data:
            if date_last == 'A':
                return 'admin'
            else:
                return 'user'
        else:
            return False

    def execute(self, query):
        self.cursor.execute(query)
        headers = [i[0] for i in self.cursor.description]
        result = self.cursor.fetchall()
        return headers, result

    def close_conn(self):
        self.cursor.close()
