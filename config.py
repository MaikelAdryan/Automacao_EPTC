import configparser
from directories import DIR_NGS

CONFIG = configparser.ConfigParser()
CONFIG.read(f'{DIR_NGS}NGS.ini')

NGS_DIR_ORACLE = CONFIG['NGS_DIR_ORACLE']
ORACLE_CLIENT = NGS_DIR_ORACLE['DIR']

EMP = NGS_DIR_ORACLE['EMP']

CONFIG_NGS = CONFIG['NGS']
ORACLE_HOST, ORACLE_PORT, ORACLE_SERVICE  = CONFIG_NGS['SQLNET']\
  .split(':')

CONFIG.read('dboracle.ini')
DB_CONFIG = CONFIG['DATABASE']

ORACLE_USER, ORACLE_PASS = DB_CONFIG['user'], DB_CONFIG['password']
