from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from login import login

URL_EPTC = 'https://156poa.procempa.com.br'
FIREFOX = Firefox

def start_firefox():
  """Função para abrir o navegador firefox

  Returns:
    webdriver.Firefox: Retorna o navegador firefox
  """
  try:
    BROWSER = FIREFOX()
    BROWSER.get(URL_EPTC)
    login()
    return BROWSER
  except:
    return 'Falha ao abrir o firefox.'


def download_excel(browser: Firefox, lote: int):
  LOTE_1, LOTE_2 = '999901074', '999901075'
  URL_FILA = f'{URL_EPTC}/sistemas/156/fila/servicos_local.php?'
  URL_EXCEL_LOTE_1 = f'{URL_FILA}cod_local_destino={LOTE_1}'
  URL_EXCEL_LOTE_2 = f'{URL_FILA}cod_local_destino={LOTE_2}'
  XPATH_EXCEL = '//html/body/table/tbody/tr[1]/th[2]/a'
  if lote == 1:
    browser.get(URL_EXCEL_LOTE_1)
    browser.find_element(By.XPATH, XPATH_EXCEL).click()
  elif lote == 2:
    browser.get(URL_EXCEL_LOTE_2)
    browser.find_element(By.XPATH, XPATH_EXCEL).click()
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
    browser.close()
    return 'Firefox fechado com sucesso.'
  except:
    return 'Falha ao fechar o Firefox.'


if __name__ == '__main__':
  browser = start_firefox()
  print(close_firefox(browser))
