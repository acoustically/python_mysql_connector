import pymysql

class Connector:
  def __init__(self, host, user, password, db):
    self.host = host
    self.user = user
    self.password = password
    self.db = db

  def __connect(self):
    connection = pymysql.connect(host=self.host,
                                 user=self.user,
                                 password=self.password,
                                 db=self.db,
                                 charset="utf8")
    return connection

  def query(self, sql):
    connection = self.__connect()
    cursor = connection.cursor()
    if self.__check_sql(sql):
      result = self.__manipulate_query(cursor, sql)
    else:
      result = self.__search_query(cursor, sql)
    connection.close()
    return result

  def __search_query(self, cursor, sql):
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

  def __manipulate_query(self, cursor, sql):
    try:
      result = cursor.execute(sql)
      cursor.fetchall()
      connection.commit()
      return result
    except Exception as error:
      return error.args

  def __check_sql(self, sql):
    return sql.find("select") == -1 and sql.find("SELECT") == -1
