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
    user=ORACLE_USER, password=ORACLE_PASS, dsn=DNS
  ) as CONNECTION:
    with CONNECTION.cursor() as CURSOR:
      QUERY = f"""select PROTOCOLO from DMB700"""
      CURSOR.execute(QUERY)
      db_protocols = CURSOR.fetchall()
      for protocol in db_protocols:
        PROTOCOLS.append(protocol[0])
  return PROTOCOLS


def insert_reclamation(reclamation: dict):
  with oracledb.connect(
    user=ORACLE_USER, password=ORACLE_PASS, dsn=DNS
  ) as CONNECTION:
    with CONNECTION.cursor() as CURSOR:
      QUERY = f"""
        INSERT INTO DMB700 (
          EMP,
          ID_SEQ,
          PROTOCOLO,
          RECLAMANTE,
          SERVICO,
          ENDERECO,
          DATA_ABERTURA,
          DATA_VENCIMENTO,
          PRAZO_DIAS,
          ATRASO_DIAS,
          LOTE,
          STPOA_LINHA,
          STPOA_SENTIDO,
          STPOA_PREFIXO,
          STPOA_MOTIVO,
          STPOA_DATA,
          STPOA_HORA,
          DESCRICAO
        ) VALUES (
          :EMP,
          S_DMB700.NEXTVAL,
          :PROTOCOLO,
          :RECLAMANTE,
          :SERVICO,
          :ENDERECO,
          TO_DATE(:DATA_ABERTURA, 'DD/MM/YYYY'),
          TO_DATE(:DATA_VENCIMENO, 'DD/MM/YYYY'),
          :PRAZO_DIAS,
          :ATRASO_DIAS,
          :LOTE,
          :STPO_LINHA,
          :STPOA_SENTIDO,
          :STPOA_PREFIXO,
          :STPOA_MOTIVO,
          TO_DATE(:STPOA_DATA, 'DD/MM/YYYY'),
          TO_DATE(:STPOA_HORA, 'HH24:MI'),
          :DESCRICAO
        )
      """
      CURSOR.execute(
        QUERY,
        EMP=reclamation['EMP'],
        PROTOCOLO=reclamation['PROTOCOLO'],
        RECLAMANTE=reclamation['RECLAMANTE'],
        SERVICO=reclamation['SERVICO'],
        ENDERECO=reclamation['ENDERECO'],
        DATA_ABERTURA=reclamation['DATA_ABERTURA'],
        DATA_VENCIMENO=reclamation['DATA_VENCIMENO'],
        PRAZO_DIAS=reclamation['PRAZO_DIAS'],
        ATRASO_DIAS=reclamation['ATRASO_DIAS'],
        LOTE=reclamation['LOTE'],
        STPO_LINHA=reclamation['STPO_LINHA'],
        STPOA_SENTIDO=reclamation['STPOA_SENTIDO'],
        STPOA_PREFIXO=reclamation['STPOA_PREFIXO'],
        STPOA_MOTIVO=reclamation['STPOA_MOTIVO'],
        STPOA_DATA=reclamation['STPOA_DATA'],
        STPOA_HORA=reclamation['STPOA_HORA'],
        DESCRICAO=reclamation['DESCRICAO']
      )
      CONNECTION.commit()


if __name__ == '__main__':
  RECLAMATION = {
    'EMP': 21,
    'PROTOCOLO': '319432-23-98',
    'RECLAMANTE': 'NAIRA AMARANTE',
    'SERVICO': 'TRIPULAÇÃO',
    'ENDERECO': 'PCA PEREIRA PAROBE',
    'DATA_ABERTURA': '04/10/2023',
    'DATA_VENCIMENO': '03/12/2023',
    'PRAZO_DIAS': '60',
    'ATRASO_DIAS': '-',
    'LOTE': 'LOTE 1',
    'STPO_LINHA': '610',
    'STPOA_SENTIDO': 'BC',
    'STPOA_PREFIXO': '6610',
    'STPOA_MOTIVO': 'TESTE_NGS',
    'STPOA_DATA': '04/10/2023',
    'STPOA_HORA': '14:30',
    'DESCRICAO': 'test'
  }
  insert_reclamation(RECLAMATION)
  # print(get_protocols())
  pass