# -*- coding: utf-8 -*-

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from excel import DIR_TEMP, clear_dir_download, move_excel
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

def start_firefox():
  """Função para abrir o navegador firefox e ir até o site da EPTC

  Returns:
    webdriver.Firefox: Retorna o navegador firefox
  """
  BROWSER = FIREFOX()
  BROWSER.get(URL_EPTC)
  return BROWSER


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


def download_and_move_excel(browser: Firefox, url: str, filename: str):
  browser.get(url)
  browser.find_element(By.XPATH, XPATH_BUTTON_DOWNLOAD_EXCEL).click()
  move_excel(filename)


def download_excel(lote: int = 0):
  clear_dir_download()
  BROWSER = start_firefox()
  try:
    match lote:
      case 1:
        download_and_move_excel(BROWSER, URL_EXCEL_LOTE_1, 'LOTE_1.xls')
      case 2:
        download_and_move_excel(BROWSER, URL_EXCEL_LOTE_2, 'LOTE_2.xls')
      case _:
        download_and_move_excel(BROWSER, URL_EXCEL_LOTE_1, 'LOTE_1.xls')
        download_and_move_excel(BROWSER, URL_EXCEL_LOTE_2, 'LOTE_2.xls')
    close_firefox(BROWSER)
  except:
    close_firefox(BROWSER)
    return 'Falha ao baixar e mover o excel!'


def get_informations_from_reclamation():
  try:
    with open(f'{DIR_TEMP}reclamations.json', 'r', encoding='utf-8') as FILE_JSON:
      RECLAMATIONS = json.load(FILE_JSON)
  except:
    return 'Falha ao abrir o json!'
  PROTOCOLS = RECLAMATIONS['PROTOCOLO']
  TOTAL = len(PROTOCOLS)
  
  match TOTAL:
    case 0:
      return 'Nada a atualizar!'
    
    case _:
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
      for protocol in PROTOCOLS:
        try:
          BROWSER.get(f'{URL_FIND_PROTOCOL}{protocol}')
          BROWSER.find_element(By.XPATH, XPATH_DETALHES_TRAMITES).click()
          text = BROWSER.find_element(By.XPATH, XPATH_TEXTAREA).text
          INFORMATIONS_PROTOCOL['DESCRICAO'].append(text)
        except:
          return 'Baixe a planilha novamente!'
        try:
          BROWSER.get(f'{URL_INFO_TRAMITE}{protocol}{RESTANT}')
          for key in INFORMATIONS_KEYS:
            if key == 'DESCRICAO':
              break
            td = BROWSER.find_element(By.XPATH, f"//td[text()='{key}']")
            text = td.find_element(By.XPATH, 'following-sibling::td').text
            INFORMATIONS_PROTOCOL[key].append(text)
        except:
          return 'Baixe a planilha novamente!'
      
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
        description = str(description).replace('\n', '').upper().strip()
        if RECEIVED_EMAIL in description:
          text = description.replace(RECEIVED_EMAIL, '').strip()
          RECEIVED.append('EMAIL')
        else:
          text = description
          RECEIVED.append('TELEFONE')
        DESCRICAO.append(text)
      RECLAMATIONS['DESCRICAO'] = DESCRICAO
      RECLAMATIONS['ORIGEM_RECLAMACAO'] = RECEIVED
      
      try:
        with open(f'{DIR_TEMP}dados.json', 'w', encoding='utf-8') as FILE:
          json.dump(RECLAMATIONS, FILE, indent=2, ensure_ascii=False)
        
        return 'Dados salvos com sucesso!'
      except:
        return 'Falha ao salvar os dados.'


if __name__ == '__main__':
  pass
