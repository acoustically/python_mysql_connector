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
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    if self.__check_sql(sql):
      result, err = self.__manipulate_query(cursor, sql)
    else:
      result, err = self.__search_query(cursor, sql)
    connection.commit()
    connection.close()
    return result, err

  def __search_query(self, cursor, sql):
    try:
      row = cursor.execute(sql)
      result = cursor.fetchall()
      if row == 0:
        return None, {"message":"not exist", "errno":1602}
      else:
        return result, None
    except Exception as error:
      return None, error

  def __manipulate_query(self, cursor, sql):
    try:
      result = cursor.execute(sql)
      cursor.fetchall()
      return result, None
    except Exception as error:
      return None, error.args

  def __check_sql(self, sql):
    return sql.find("select") == -1 and sql.find("SELECT") == -1
