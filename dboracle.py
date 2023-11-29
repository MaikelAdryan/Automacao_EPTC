import oracledb
import configparser

FILE_CONFIG = 'dboracle.ini'
CONFIG = configparser.ConfigParser()
CONFIG.read(FILE_CONFIG)
DB_CONFIG = CONFIG['database']

ORACLE_CLIENT = DB_CONFIG['client_oracle']
oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT)

ORACLE_USER, ORACLE_PASS = DB_CONFIG['user'], DB_CONFIG['password']
ORACLE_HOST, ORACLE_PORT = DB_CONFIG['host'], DB_CONFIG['port']
ORACLE_SERVICE = DB_CONFIG['service']
DNS = oracledb.makedsn(
  host=ORACLE_HOST, port=ORACLE_PORT, service_name=ORACLE_SERVICE)

def get_protocols():
  """Pega todos os protocolos do banco de dados.

  Returns:
    PROTOCOLS (list): Lista contendo todos os protocolos
  """
  PROTOCOLS = []
  with oracledb.connect(
    user=ORACLE_USER, password=ORACLE_PASS, dsn=DNS) as CONNECTION:
    with CONNECTION.cursor() as CURSOR:
      QUERY = f"""select PROTOCOLO from {DB_CONFIG['table']}"""
      CURSOR.execute(QUERY)
      db_protocols = CURSOR.fetchall()
      for protocol in db_protocols:
        PROTOCOLS.append(protocol[0])
  return PROTOCOLS


if __name__ == '__main__':
  print(get_protocols())
  pass