from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from move_excel import clear_dir_excel
from login import USER, PASSWORD

URL_EPTC = f'https://{USER}:{PASSWORD}@156poa.procempa.com.br'
URL_FILA = f'{URL_EPTC}/sistemas/156/fila/servicos_local.php?'
LOTE_1, LOTE_2 = '999901074', '999901075'
URL_EXCEL_LOTE_1 = f'{URL_FILA}cod_local_destino={LOTE_1}'
URL_EXCEL_LOTE_2 = f'{URL_FILA}cod_local_destino={LOTE_2}'
XPATH_BUTTON_DOWNLOAD_EXCEL = '//html/body/table/tbody/tr[1]/th[2]/a'
FIREFOX = Firefox

def start_firefox():
  """Função para abrir o navegador firefox

  Returns:
    webdriver.Firefox: Retorna o navegador firefox
  """
  try:
    BROWSER = FIREFOX()
    BROWSER.get(URL_EPTC)
    return BROWSER
  except:
    return 'Falha ao abrir o firefox.'


def download_excel(lote: int):
  BROWSER = start_firefox()
  clear_dir_excel()
  
  if lote == 1:
    BROWSER.get(URL_EXCEL_LOTE_1)
    BROWSER.find_element(By.XPATH, XPATH_BUTTON_DOWNLOAD_EXCEL).click()
    close_firefox(BROWSER)
  elif lote == 2:
    BROWSER.get(URL_EXCEL_LOTE_2)
    BROWSER.find_element(By.XPATH, XPATH_BUTTON_DOWNLOAD_EXCEL).click()
    close_firefox(BROWSER)
  else:
    return 'Lote inválido!'


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
  browser = start_firefox()
  print(close_firefox(browser))
