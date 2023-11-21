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

def clear_dir_download():
  try:
    for excel in os.listdir(DIR_DOWNLOAD):
      if excel.startswith(FILENAME):
        os.remove(f'{DIR_DOWNLOAD}/{excel}')
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


def read_excel(excel: str):
	lote = 'LOTE 1' if excel == 'LOTE_1.xls' else 'LOTE 2'
	try:
		with open(f'temp/{excel}', 'r') as file:
			return [lote, BeautifulSoup(file.read(), 'html.parser')]
	except:
		return 'Arquivo não encontrado'


def extract_values_of_excel(lote_and_excel_readed: [str, BeautifulSoup]):
	lote, excel_readed = lote_and_excel_readed
	RECLAMAÇÕES = {
		'Protocolo': [],
		'Reclamante': [],
		'Serviço': [],
		'Endereço': [],
		'Data Abertura': [],
		'Data Vencimento': [],
		'Prazo (dias)': [],
		'Atraso(dias)': [],
	# 'Lote': [],
	# 'Descrição': []
	}
	KEYS = RECLAMAÇÕES.keys()
	tds = excel_readed.find_all('td')
	for i, key in enumerate(KEYS):
		values = [td.text.strip().replace('\n', '') for td in tds[i::8]]
		RECLAMAÇÕES[key] = values
	
	total = len(RECLAMAÇÕES['Protocolo'])

	RECLAMAÇÕES['Lote'] = [lote] * total

	for key in KEYS:
		if len(RECLAMAÇÕES[key]) != total:
			return f'O total de {key}: {len(RECLAMAÇÕES[key])} não bateu com {total}'

	return RECLAMAÇÕES


if __name__ == '__main__':
  # move_excel('LOTE_1')
	# print(DIR_TEMP)
	lote_1 = read_excel('LOTE_1.xls')
	lote_2 = read_excel('LOTE_2.xls')
	# protocols = extract_protocol_in_excel(read)
	print(extract_values_of_excel(lote_1))
	print(extract_values_of_excel(lote_2))