# -*- coding: utf-8 -*-

import os
from shutil import move
from bs4 import BeautifulSoup

DIR_ACTUAL = os.getcwd().replace('\\','/')
DIR_TEMP = f'{DIR_ACTUAL}/temp/'

USER_PATH = os.path.expanduser('~')
DIR_DOWNLOAD = f'{USER_PATH}/Downloads'
FILENAME = 'protocolos_por_fila'
DIR_EXCEL = f'{DIR_DOWNLOAD}/{FILENAME}'

REFACTOR_SERVICES = lambda service: service.split(' - ')[-1]
REFACTOR_ADDRESSS = lambda address: address.split(' ,')[0]
REFACTOR_PROTOCOL = lambda protocol: protocol.replace('\n', '')

def contains_excel_in_dir_download():
  for excel in os.listdir(DIR_DOWNLOAD):
    if excel.startswith(FILENAME):
      return True
    return False


def clear_dir_download():
  if contains_excel_in_dir_download():
    for excel in os.listdir(DIR_DOWNLOAD):
      os.remove(f'{DIR_DOWNLOAD}/{excel}')
    return 'Limpo com sucesso!'
  else:
    return 'Falha ao limpar diretório de downloads.'


def move_excel(lote: str):
  try:
    move(f'{DIR_EXCEL}.xls', f'{DIR_TEMP}{lote}.xls')
    return ['green', f'Atualizado com sucesso!']
  except:
    return ['red', 'Arquivo não encontrado!']


def read_excel(excel: str):
  lote = 'LOTE 1' if excel == 'LOTE_1.xls' else 'LOTE 2'
  try:
    with open(f'./temp/{excel}', 'r') as file:
      return [lote, BeautifulSoup(file.read(), 'html.parser')]
  except:
    return 'Arquivo não encontrado'


def extract_values_of_excel(lote_and_excel_readed):
  if lote_and_excel_readed == 'Arquivo não encontrado':
    return ['red', lote_and_excel_readed]
  
  lote, excel_readed = lote_and_excel_readed
  RECLAMAÇÕES = {
    'PROTOCOLO': [],
    'RECLAMANTE': [],
    'SERVIÇO': [],
    'ENDEREÇO': [],
    'DATA_ABERTURA': [],
    'DATA_VENCIMENTO': [],
    'PRAZO_DIAS': [],
    'ATRASO_DIAS': [],
  # 'LOTE': [],
  # 'DESCRIÇÃO': []
  }

  KEYS = RECLAMAÇÕES.keys()
  tds = excel_readed.find_all('td')
  for i, key in enumerate(KEYS):
    values = [str(td.text).strip().upper() for td in tds[i::8]]
    RECLAMAÇÕES[key] = values
    
  total = len(RECLAMAÇÕES['PROTOCOLO'])

  for key in KEYS:
    if len(RECLAMAÇÕES[key]) != total:
      return f'{key}: {len(RECLAMAÇÕES[key])} não bateu com {total}'

  RECLAMAÇÕES['PROTOCOLO'] = list(map(REFACTOR_PROTOCOL, RECLAMAÇÕES['PROTOCOLO']))
  RECLAMAÇÕES['SERVIÇO'] 	 = list(map(REFACTOR_SERVICES, RECLAMAÇÕES['SERVIÇO']))
  RECLAMAÇÕES['ENDEREÇO']  = list(map(REFACTOR_ADDRESSS, RECLAMAÇÕES['ENDEREÇO']))
  RECLAMAÇÕES['LOTE'] = [lote] * total

  return RECLAMAÇÕES


def merged_excels(LOTE_1: dict, LOTE_2: dict):
  LOTE_1_KEYS, LOTE_2_KEYS = LOTE_1.keys(), LOTE_2.keys()
  if LOTE_1_KEYS == LOTE_2_KEYS:
    RECLAMATIONS = {}
    for key in LOTE_1_KEYS:
      RECLAMATIONS[key] =  LOTE_1[key] + LOTE_2[key]
    return RECLAMATIONS
  else:
    return (
      f'Lote 1 tem {len(LOTE_1_KEYS)} chaves e'
      f'lote 2 tem {len(LOTE_2_KEYS)} chaves.'
    )

def fazer_magia():
  lote_1 = read_excel('LOTE_1.xls')
  lote_2 = read_excel('LOTE_2.xls')
  dict_lote1 = extract_values_of_excel(lote_1)
  dict_lote2 = extract_values_of_excel(lote_2)
  # dict_ = merged_excels(dict_lote1, dict_lote2)
  return dict_lote1


if __name__ == '__main__':
  # fazer_magia()
  # move_excel('LOTE_1')
  # print(DIR_TEMP)
  # lote_2 = read_excel('LOTE_2.xls')
  # protocols = extract_protocol_in_excel(read)
  # lotes = dict_lote1.update(dict_lote2)
  # print(lotes)
  # print(extract_values_of_excel(lote_1))
  # lote_1 = read_excel('LOTE_1.xls')
  # dict_lote1 = extract_values_of_excel(lote_1)
  # get_protocols(dict_lote1)
  # lote_2 = read_excel('LOTE_2.xls')
  # dict_lote2 = extract_values_of_excel(lote_2)
  # dict_ = merged_excels(dict_lote1, dict_lote2)
  # get_protocols(dict_)
  pass