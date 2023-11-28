from login_dboracle import UN, CS, PW
import oracledb

with oracledb.connect(user=UN, password=PW, dsn=CS) as connection:
  with connection.cursor() as cursor:
    sql = """select sysdate from dual"""
  for response in cursor.execute(sql):
    print(response)
