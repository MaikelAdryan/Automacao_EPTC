import oracledb
import configparser
from json import load

from diretories import DIR_NGS, clear_file
from logs import write_log
 
FILE_NGS_CONFIG = f'{DIR_NGS}NGS.ini'
CONFIG = configparser.ConfigParser()
CONFIG.read(FILE_NGS_CONFIG)

NGS_DIR_ORACLE = CONFIG['NGS_DIR_ORACLE']
ORACLE_CLIENT = NGS_DIR_ORACLE['DIR']
oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT)

CONFIG_NGS = CONFIG['NGS']
ORACLE_HOST, ORACLE_PORT, ORACLE_SERVICE  = CONFIG_NGS['SQLNET']\
  .split(':')

FILE_CONFIG = 'dboracle.ini'
CONFIG.read(FILE_CONFIG)
DB_CONFIG = CONFIG['DATABASE']

ORACLE_USER, ORACLE_PASS = DB_CONFIG['user'], DB_CONFIG['password']

DNS = oracledb.makedsn(
  host=ORACLE_HOST, port=ORACLE_PORT, service_name=ORACLE_SERVICE)

QUERY_GET_USER_PASS = '''
SELECT
  (
    SELECT
      comandos
    FROM
      dg0080
    WHERE
      emp = 21
      AND sistema = 'SISEST'
      AND opcao = 'LOGIN_EPTC'
) login,
  (
    SELECT
      comandos
    FROM
      dg0080
    WHERE
      emp = 21
      AND sistema = 'SISEST'
      AND opcao = 'PASS_EPTC'
  ) pass
FROM
  dual
'''

QUERY_INSERT_RECLAMATION = f'''
INSERT INTO dmb700 (
  emp,
  id_seq,
  protocolo,
  reclamante,
  servico,
  endereco,
  data_abertura,
  data_vencimento,
  prazo_dias,
  atraso_dias,
  lote,
  stpoa_linha,
  stpoa_sentido,
  stpoa_prefixo,
  stpoa_motivo,
  stpoa_data,
  stpoa_hora,
  descricao,
  origem_reclamacao
) VALUES (
  :emp,
  s_dmb700.NEXTVAL,
  :protocolo,
  :reclamante,
  :servico,
  :endereco,
  :data_abertura,
  :data_vencimeno,
  :prazo_dias,
  :atraso_dias,
  :lote,
  :stpo_linha,
  :stpoa_sentido,
  :stpoa_prefixo,
  :stpoa_motivo,
  :stpoa_data,
  :stpoa_hora,
  :descricao,
  :origem_reclamacao
)
'''

def get_user_and_password():
  '''Função para pegar o usuário e a senha no banco de dados

  Returns:
    LOGIN (USER, PASSWORD): Usuário e senha do login
  '''
  with oracledb.connect(
    user=ORACLE_USER, password=ORACLE_PASS, dsn=DNS
  ) as CONNECTION:
    with CONNECTION.cursor() as CURSOR:
      CURSOR.execute(QUERY_GET_USER_PASS)
      LOGIN = CURSOR.fetchall()[0]
      USER, PASSWORD = LOGIN
  return USER, PASSWORD


def get_protocols():
  '''Pega todos os protocolos do banco de dados.

  Returns:
    PROTOCOLS (list): Lista contendo todos os protocolos
  '''
  PROTOCOLS = []
  with oracledb.connect(
    user=ORACLE_USER, password=ORACLE_PASS, dsn=DNS
  ) as CONNECTION:
    with CONNECTION.cursor() as CURSOR:
      QUERY = f'''select PROTOCOLO from DMB700'''
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
      CURSOR.execute(
        QUERY_INSERT_RECLAMATION,
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
  except:
    return 'Falha ao carregar os dados.'
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
    except:
      write_log(f'Falha ao inserir o protocolo {JSON["PROTOCOLO"]}')
      return
  clear_file('dados')
  write_log(f'Incluidos {TOTAL} protocolos.')


if __name__ == '__main__':
  pass