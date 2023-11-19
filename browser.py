from selenium.webdriver import Firefox

FIREFOX = Firefox

def start_firefox():
  """Função para abrir o navegador firefox

  Returns:
    webdriver.Firefox: Retorna o navegador firefox
  """
  try:
    BROWSER = FIREFOX()
    return BROWSER
  except:
    return 'Falha ao abrir o firefox.'


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
