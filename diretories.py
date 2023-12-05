import os

DIR_ACTUAL = os.getcwd().replace('\\', '/')
DIR_TEMP = f'{DIR_ACTUAL}/temp/'

USER_PATH = os.path.expanduser('~').replace('\\', '/')
DIR_DOWNLOAD = f'{USER_PATH}/Downloads'

DIR_NGS = f'{DIR_ACTUAL.split("/")[0]}/NGS/SERVICES/'
DIR_LOGS = f'{DIR_NGS}logs/'

def clear_file(file: str):
  try:
    with open(f'{DIR_TEMP}{file}.json', 'w', encoding='utf-8') as FILE:
      FILE.write('')
  except:
    print('An exception occurred')
