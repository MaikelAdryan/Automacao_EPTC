# -*- coding: utf-8 -*-

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from excel import (
  DIR_TEMP, clear_dir_download, move_excel)
from login_eptc import USER, PASSWORD
import json

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

FILE_NAME = 'dados.json'

def start_firefox():
  """Função para abrir o navegador firefox e ir até o site da EPTC

  Returns:
    webdriver.Firefox: Retorna o navegador firefox
  """
  BROWSER = FIREFOX()
  BROWSER.get(URL_EPTC)
  return BROWSER


def goto_url_download(URL_LOTE: str):
  """Função que abre o site da EPTC, baixa o excel e fecha o navegador
  
  Args:
    URL_LOTE (str): Baixa a planilha com base no lote
  
  Returns:
    [color, text]: a cor a ser preenchida e mensagem de falha ou sucesso
  """
  try:
    BROWSER = start_firefox()
    BROWSER.get(URL_LOTE)
    BROWSER.find_element(By.XPATH, XPATH_BUTTON_DOWNLOAD_EXCEL).click()
    close_firefox(BROWSER)
    return ['green', 'Sucesso!']
  except:
    return ['red', 'Falha ao baixar.']


def download_excel(lote: int):
  """Função para ir até o site da Eptc e baixar as planilhas do excel 
  para extrair os dados das mesmas.
  
  Args:
    lote (int): Número do lote para baixar a planilha
  
  Returns:
    [color, text]: a cor a ser preenchida e mensagem de falha ou sucesso
  """
  clear_dir_download()
  moved  = ''
  match lote:
    case 1:
      goto_url_download(URL_EXCEL_LOTE_1)
      moved = move_excel('LOTE_1.xls')
    case 2:
      goto_url_download(URL_EXCEL_LOTE_2)
      moved = move_excel('LOTE_2.xls')
    case _ :
      return ['red', 'Falha ao baixar excel!']
  return ['green', f'Excel LOTE {lote} {moved}!']


def get_informations_from_reclamation():
  """Função para pegar as informações da reclamação

  Returns:
    message [cor, mensagem]: retorna uma mensagem de erro e falha
  """
  try:
    from reclamations import RECLAMATIONS
  except:
    return ['red', 'arquivos não encontrados']

  PROTOCOLS = RECLAMATIONS['PROTOCOLO']
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
  TOTAL = len(PROTOCOLS)

  if TOTAL > 0:
    BROWSER = start_firefox()
    for protocol in PROTOCOLS:
      try:
        BROWSER.get(f'{URL_FIND_PROTOCOL}{protocol}')
        BROWSER.find_element(By.XPATH, XPATH_DETALHES_TRAMITES).click()
        text = BROWSER.find_element(By.XPATH, XPATH_TEXTAREA).text
        INFORMATIONS_PROTOCOL['DESCRICAO'].append(text)
      except:
        return ['red', 'Baixe a planilha novamente!']
      try:
        BROWSER.get(f'{URL_INFO_TRAMITE}{protocol}{RESTANT}')
        for key in INFORMATIONS_KEYS:
          if key == 'DESCRICAO':
            break
          td = BROWSER.find_element(By.XPATH, f"//td[text()='{key}']")
          text = td.find_element(By.XPATH, 'following-sibling::td').text
          INFORMATIONS_PROTOCOL[key].append(text)
      except:
        return ['red', 'Baixe a planilha novamente!']
    
    close_firefox(BROWSER)
    
    for key in INFORMATIONS_KEYS:
      TOTAL_KEY = len(INFORMATIONS_PROTOCOL[key])
      if TOTAL != TOTAL_KEY:
        return f'Total não bate! {key} com {TOTAL_KEY} valores é dife'+\
          f'rente de {TOTAL}.'
      else:
        RECLAMATIONS[key] = INFORMATIONS_PROTOCOL[key]
    
    # EMP = []
    # for car in RECLAMATIONS['STPOA_PREFIXO']:
    #   if car.startswith(('66', '67', '68')):
    #     EMP.append(1)
    #   elif car.startswith(('64', '65')):
    #     EMP.append(3)
    #   elif car.startswith('61'):
    #     EMP.append(4)
    #   else:
    #     EMP.append(21)
    # RECLAMATIONS['EMP'] = EMP
    RECLAMATIONS['EMP'] = [21] * TOTAL

    RECLAMATIONS['STPOA_MOTIVO'] = [
      motive.upper() for motive in RECLAMATIONS['STPOA_MOTIVO']
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
        case 'TerminalBairroTerminal':
          text = 'TT'
      SENTIDO.append(text)
    RECLAMATIONS['STPOA_SENTIDO'] = SENTIDO
    
    DESCRICAO = []
    RECEIVED = []
    RECEIVED_EMAIL = '[RECLAMAÇÃO RECEBIDA POR E-MAIL]'
    for description in RECLAMATIONS['DESCRICAO']:
      description = description.replace('\n', '').upper()
      if RECEIVED_EMAIL in description:
        text = description.replace(RECEIVED_EMAIL, '')
        RECEIVED.append('EMAIL')
      else:
        text = description
        RECEIVED.append('TELEFONE')
      DESCRICAO.append(text)
    RECLAMATIONS['DESCRICAO'] = DESCRICAO
    RECLAMATIONS['ORIGEM_RECLAMACAO'] = RECEIVED
    
    try:
      with open(f'{DIR_TEMP}{FILE_NAME}', 'w', encoding='utf-8') as FILE:
        json.dump(RECLAMATIONS, FILE, indent=2, ensure_ascii=False)
      
      return ['green', 'Dados salvos com sucesso!']
    except:
      return ['red', 'Falha ao salvar os dados.']


def close_firefox(browser: Firefox):
  """Função para fechar o navegador Firefox já aberto antes

  Args:
    browser (Firefox): Navegador aberto pelafunção start_firefox

  Returns:
    message (str): Falha ou Sucesso!
  """
  try:
    browser.quit()
    return 'Firefox fechado com sucesso.'
  except:
    return 'Falha ao fechar o Firefox.'


if __name__ == '__main__':
  get_informations_from_reclamation()
  pass
