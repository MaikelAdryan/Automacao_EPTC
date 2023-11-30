import oracledb
import configparser
from json import load

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
          DESCRICAO,
          ORIGEM_RECLAMACAO
        ) VALUES (
          :EMP,
          S_DMB700.NEXTVAL,
          :PROTOCOLO,
          :RECLAMANTE,
          :SERVICO,
          :ENDERECO,
          :DATA_ABERTURA,
          :DATA_VENCIMENO,
          :PRAZO_DIAS,
          :ATRASO_DIAS,
          :LOTE,
          :STPO_LINHA,
          :STPOA_SENTIDO,
          :STPOA_PREFIXO,
          :STPOA_MOTIVO,
          :STPOA_DATA,
          :STPOA_HORA,
          :DESCRICAO,
          :ORIGEM_RECLAMACAO
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
        STPO_LINHA=reclamation['STPOA_LINHA'],
        STPOA_SENTIDO=reclamation['STPOA_SENTIDO'],
        STPOA_PREFIXO=reclamation['STPOA_PREFIXO'],
        STPOA_MOTIVO=reclamation['STPOA_MOTIVO'],
        STPOA_DATA=reclamation['STPOA_DATA'],
        STPOA_HORA=reclamation['STPOA_HORA'],
        DESCRICAO=reclamation['DESCRICAO'],
        ORIGEM_RECLAMACAO=reclamation['ORIGEM_RECLAMACAO']
      )
      CONNECTION.commit()


def send_reclamation_to_dboracle():
  RECLAMATIONS, TOTAL = {}, 0
  try:
    with open('temp/dados.json', 'r', encoding='utf-8') as FILE_JSON:
      RECLAMATIONS = load(FILE_JSON)
      TOTAL = len(RECLAMATIONS['PROTOCOLO'])
      # print(RECLAMATIONS['PROTOCOLO'])
      # insert_reclamation()
  except:
    return ['red', 'Falha ao carregar os dados.']
  for i in range(TOTAL):
    JSON = {
      'EMP': RECLAMATIONS['EMP'][i],
      'PROTOCOLO': RECLAMATIONS['PROTOCOLO'][i],
      'RECLAMANTE': RECLAMATIONS['RECLAMANTE'][i],
      'SERVICO': RECLAMATIONS['SERVIÇO'][i],
      'ENDERECO': RECLAMATIONS['ENDEREÇO'][i],
      'DATA_ABERTURA': RECLAMATIONS['DATA_ABERTURA'][i],
      'DATA_VENCIMENO': RECLAMATIONS['DATA_VENCIMENTO'][i],
      'PRAZO_DIAS': RECLAMATIONS['PRAZO_DIAS'][i],
      'ATRASO_DIAS': RECLAMATIONS['ATRASO_DIAS'][i],
      'LOTE': RECLAMATIONS['LOTE'][i],
      'STPOA_LINHA': RECLAMATIONS['STPOA_LINHA'][i],
      'STPOA_SENTIDO': RECLAMATIONS['STPOA_SENTIDO'][i],
      'STPOA_PREFIXO': RECLAMATIONS['STPOA_PREFIXO'][i],
      'STPOA_MOTIVO': RECLAMATIONS['STPOA_MOTIVO'][i],
      'STPOA_DATA': RECLAMATIONS['STPOA_DATA'][i],
      'STPOA_HORA': RECLAMATIONS['STPOA_HORA'][i],
      'DESCRICAO': RECLAMATIONS['DESCRICAO'][i],
      'ORIGEM_RECLAMACAO': RECLAMATIONS['ORIGEM_RECLAMACAO'][i]
    }
    try:
      insert_reclamation(JSON)
      print(f'{i} concluido')
    except:
      print('An exception occurred')



if __name__ == '__main__':
  print(send_reclamation_to_dboracle())
  # RECLAMATION = {
  #   'EMP': 21,
  #   'PROTOCOLO': '319432-23-98',
  #   'RECLAMANTE': 'NAIRA AMARANTE',
  #   'SERVICO': 'TRIPULAÇÃO',
  #   'ENDERECO': 'PCA PEREIRA PAROBE',
  #   'DATA_ABERTURA': '04/10/2023',
  #   'DATA_VENCIMENO': '03/12/2023',
  #   'PRAZO_DIAS': '60',
  #   'ATRASO_DIAS': '-',
  #   'LOTE': 'LOTE 1',
  #   'STPOA_LINHA': '610',
  #   'STPOA_SENTIDO': 'BC',
  #   'STPOA_PREFIXO': '6610',
  #   'STPOA_MOTIVO': 'TESTE_NGS',
  #   'STPOA_DATA': '04/10/2023',
  #   'STPOA_HORA': '14:30',
  #   'DESCRICAO': 'test',
  #   'ORIGEM_RECLAMACAO': 'test'
  # }
  # insert_reclamation(RECLAMATION)
  # print(get_protocols())
  pass