import os
from shutil import move

DIR_ACTUAL = os.getcwd()
DIR_TEMP = f'{DIR_ACTUAL}\\temp\\'

USER_PATH = os.path.expanduser('~')
DIR_DOWNLOAD = f'{USER_PATH}\Downloads'
FILENAME = 'protocolos_por_fila.xls'
DIR_EXCEL = f'{DIR_DOWNLOAD}\{FILENAME}'

def clear_dir_excel():
  try:
    for excel in os.listdir(DIR_DOWNLOAD):
      if excel.startswith(FILENAME):
        os.remove(f'{DIR_DOWNLOAD}\{excel}')
    return 'Limpo com sucesso!'
  except:
    return 'Falha ao limpar diretório de downloads.'


def move_excel(lote: str):
  try:
    if os.path.exists(DIR_EXCEL):
      move(DIR_EXCEL, f'{DIR_TEMP}{lote}.xls')
    return 'Movido com sucesso!'
  except:
    return 'Arquivo não encontrados!'


if __name__ == '__main__':
  # clear_dir_excel()
  # exists = os.path.exists(f'{DIR_DOWNLOAD}\{FILENAME}')
  # print(exists)
  # print(get_dir_excel())
  # print(DIR_ACTUAL)
  # dir_excel = get_dir_excel()
  print(move_excel('LOTE_1'))