# -*- coding: utf-8 -*-

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from excel import clear_dir_download, move_excel
from directories import DIR_TEMP, clear_file
import json

from dboracle import get_user_and_password, send_reclamation_to_dboracle
from logs import write_log
USER, PASSWORD = get_user_and_password()

URL_EPTC = f'https://{USER}:{PASSWORD}@156poa.procempa.com.br'
URL_FILA = f'{URL_EPTC}/sistemas/156/fila/servicos_local.php?'
LOTE_1, LOTE_2 = '999901074', '999901075'
URL_EXCEL_LOTE_1 = f'{URL_FILA}cod_local_destino={LOTE_1}'
URL_EXCEL_LOTE_2 = f'{URL_FILA}cod_local_destino={LOTE_2}'
XPATH_BUTTON_DOWNLOAD_EXCEL = '//html/body/table/tbody/tr[1]/th[2]/a'
FIREFOX = Firefox

URL_FIND_PROTOCOL = (
  f'{URL_EPTC}/Sistemas/156/fila/fila_01.php?modo=4&protocolo=')
XPATH_DETALHES_TRAMITES = '//html/body/table[4]/tbody/tr/td/a[1]'
XPATH_TEXTAREA = '//textarea'
URL_INFO_TRAMITE = (
  f'{URL_EPTC}/Sistemas/156/fila/visualiza_info.php?protocolo=')
RESTANT = '&seq_tramita=0&fase=0&cod_tramite=0'

def start_firefox():
  '''Função para abrir o navegador firefox e ir até o site da EPTC

  Returns:
    webdriver.Firefox: Retorna o navegador firefox
  '''
  try:
    BROWSER = FIREFOX()
    BROWSER.get(URL_EPTC)
    return BROWSER
  except:
    write_log('Falha ao abrir o Firefox!')


def close_firefox(browser: Firefox):
  '''Função para fechar o navegador Firefox já aberto antes

  Args:
    browser (Firefox): Navegador aberto pelafunção start_firefox
  '''
  try:
    browser.quit()
  except:
    write_log('Falha ao fechar o navegador Firefox!')
    return


def download_excel():
  clear_dir_download()
  BROWSER = start_firefox()
  try:
    BROWSER.get(URL_EXCEL_LOTE_1)
    BROWSER.find_element(By.XPATH, XPATH_BUTTON_DOWNLOAD_EXCEL).click()
    move_excel('LOTE_1.xls')
  except:
    write_log(f'Falha ao baixar e mover o excel do lote 1!')
  try:
    BROWSER.get(URL_EXCEL_LOTE_2)
    BROWSER.find_element(By.XPATH, XPATH_BUTTON_DOWNLOAD_EXCEL).click()
    move_excel('LOTE_2.xls')
  except:
    write_log(f'Falha ao baixar e mover o excel do lote 1!')
  return close_firefox(BROWSER)


def get_informations_from_reclamation_and_insert_to_db():
  try:
    with open(
      f'{DIR_TEMP}reclamations.json', 'r', encoding='utf-8') as FILE_JSON:
      RECLAMATIONS = json.load(FILE_JSON)
    clear_file('reclamations')
  except:
    return
  
  INFORMATIONS_PROTOCOL = {
    'STPOA_LINHA': [],
    'STPOA_SENTIDO': [],
    'STPOA_PREFIXO': [],
    'STPOA_MOTIVO': [],
    'STPOA_DATA': [],
    'STPOA_HORA': [],
    'DESCRICAO': []
  }
  INFORMATIONS_KEYS = INFORMATIONS_PROTOCOL.keys()
  BROWSER = start_firefox()
  
  PROTOCOLS = RECLAMATIONS['PROTOCOLO']
  for protocol in PROTOCOLS:
    try:
      BROWSER.get(f'{URL_FIND_PROTOCOL}{protocol}')
      BROWSER.find_element(By.XPATH, XPATH_DETALHES_TRAMITES).click()
      text = BROWSER.find_element(By.XPATH, XPATH_TEXTAREA).text
      INFORMATIONS_PROTOCOL['DESCRICAO'].append(text)
    except:
      write_log(f'Falha ao localizar descrição do protocolo: {protocol}!')
      return
    
    try:
      BROWSER.get(f'{URL_INFO_TRAMITE}{protocol}{RESTANT}')
      for key in INFORMATIONS_KEYS:
        if key == 'DESCRICAO':
          break
        td = BROWSER.find_element(By.XPATH, f"//td[text()='{key}']")
        text = td.find_element(By.XPATH, 'following-sibling::td').text
        INFORMATIONS_PROTOCOL[key].append(text)
    except:
      write_log(f'Falha ao localizar descrição do protocolo: {protocol}!')
      return
  
  close_firefox(BROWSER)
  TOTAL = len(PROTOCOLS)
  for key in INFORMATIONS_KEYS:
    TOTAL_KEY = len(INFORMATIONS_PROTOCOL[key])
    if TOTAL != TOTAL_KEY:
      message_error = f'Total não bate! {key} com {TOTAL_KEY} valores é'+\
      f' diferente do total de {TOTAL}.'
      write_log(message_error)
      return 
    else:
      RECLAMATIONS[key] = INFORMATIONS_PROTOCOL[key]
      
  RECLAMATIONS['EMP'] = [21] * TOTAL

  RECLAMATIONS['STPOA_MOTIVO'] = [
    str(motive).upper() for motive in RECLAMATIONS['STPOA_MOTIVO']
  ]

  SENTIDO = []
  for sentido in RECLAMATIONS['STPOA_SENTIDO']:
    match sentido:
      case 'BairroCentro':
        text = '1'
      case 'CentroBairro':
        text = '2'
      case 'BairroCentroBairro':
        text = 'BB'
      case 'CentroBairroCentro':
        text = 'CC'
      case 'TerminalBairro':
        text = 'TB'
      case 'BairroTerminal':
        text = 'BT'
      case 'TerminalBairroTerminal':
        text = 'TT'
    SENTIDO.append(text)
  RECLAMATIONS['STPOA_SENTIDO'] = SENTIDO
  
  DESCRICAO, RECEIVED = [], []
  RECEIVED_EMAIL = '[RECLAMAÇÃO RECEBIDA POR E-MAIL]'
  for description in RECLAMATIONS['DESCRICAO']:
    description = str(description).replace('\n', '').upper().strip()
    if RECEIVED_EMAIL in description:
      text, received = description.replace(RECEIVED_EMAIL, '')\
        .strip(), 'EMAIL'
    else:
      text, received = description, 'TELEFONE'
    DESCRICAO.append(text)
    RECEIVED.append(received)
    
  RECLAMATIONS['DESCRICAO'] = DESCRICAO
  RECLAMATIONS['ORIGEM_RECLAMACAO'] = RECEIVED
  
  try:
    with open(f'{DIR_TEMP}dados.json', 'w', encoding='utf-8') as FILE:
      json.dump(RECLAMATIONS, FILE, indent=2, ensure_ascii=False)
    send_reclamation_to_dboracle()
  except:
    write_log(f'Falha ao salvar os dados no arquivo dados.json!')
    return


if __name__ == '__main__':
  pass
