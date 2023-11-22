from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from excel import contains_excel_in_dir_download, clear_dir_download, fazer_magia
from login import USER, PASSWORD

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

XPATH_LINHA = '//html/body/form/table[3]/tbody/tr[3]/td[2]'
XPATH_SENTIDO = '//html/body/form/table[3]/tbody/tr[4]/td[2]'
XPATH_PREFIXO = '//html/body/form/table[3]/tbody/tr[6]/td[2]'
XPATH_OPERADOR = '//html/body/form/table[3]/tbody/tr[8]/td[2]'
XPATH_MOTIVO = '//html/body/form/table[3]/tbody/tr[9]/td[2]'
XPATH_DATA = '//html/body/form/table[3]/tbody/tr[10]/td[2]'
XPATH_HORA = '//html/body/form/table[3]/tbody/tr[11]/td[2]'


def start_firefox():
  """Função para abrir o navegador firefox e ir até o site da EPTC

  Returns:
    webdriver.Firefox: Retorna o navegador firefox
  """
  try:
    BROWSER = FIREFOX()
    BROWSER.get(URL_EPTC)
    return BROWSER
  except:
    return 'Falha ao abrir o firefox.'


def goto_url_download(URL_LOTE: str):
	"""Função que abre o site da EPTC, baixa o excel e fecha o navegador

	Args:
	URL_LOTE (str): Baixa a planilha com base no lote
	"""
	try:
		BROWSER = start_firefox()
		BROWSER.get(URL_LOTE)
		BROWSER.find_element(By.XPATH, XPATH_BUTTON_DOWNLOAD_EXCEL).click()
		close_firefox(BROWSER)
		return 'Sucesso!'
	except:
		return 'Falha ao baixar.'


def download_excel(lote: int):
	"""Função para ir até o site da Eptc e baixar as planilhas do excel para extrair os dados das mesmas.

	Args:
		lote (int): Número do lote para baixar a planilha

	Returns:
		response (list[color, text]): Retorna uma resposta se concluido ou falha e a cor respectiva
	"""
	clear_dir_download()
	match lote:
		case 1:
			goto_url_download(URL_EXCEL_LOTE_1)
			if contains_excel_in_dir_download():
				response = ['green', 'Excel lote 1 baixado com sucesso!']
		case 2:
			goto_url_download(URL_EXCEL_LOTE_2)
			if contains_excel_in_dir_download():
				response = ['green', 'Excel lote 2 baixado com sucesso!']
		case _ :
			response = ['red', 'Lote inválido!']
	return response


def get_protocols(RECLAMATIONS: dict):
	PROTOCOLS = RECLAMATIONS['PROTOCOLO']
	DESCRIÇÃO = []
	STPOA_LINHA = []
	STPOA_SENTIDO = []
	STPOA_PREFIXO = []
	STPOA_OPERADOR = []
	STPOA_MOTIVO = []
	STPOA_DATA = []
	STPOA_HORA = []
	if len(PROTOCOLS) > 0:
		BROWSER = start_firefox()
		for protocol in PROTOCOLS:
			BROWSER.get(f'{URL_FIND_PROTOCOL}{protocol}')
			BROWSER.find_element(By.XPATH, XPATH_DETALHES_TRAMITES).click()
			text = BROWSER.find_element(By.XPATH, XPATH_TEXTAREA).text
			DESCRIÇÃO.append(text)

			URL_INFO_TRAMITE = f'{URL_EPTC}/Sistemas/156/fila/visualiza_info.php?protocolo={protocol}&seq_tramita=0&fase=0&cod_tramite=0'
			BROWSER.get(URL_INFO_TRAMITE)

			

			# text = BROWSER.find_element(By.XPATH, XPATH_LINHA).text
			# STPOA_LINHA.append(text)
			# text = BROWSER.find_element(By.XPATH, XPATH_SENTIDO).text
			# STPOA_SENTIDO.append(text)
			# text = BROWSER.find_element(By.XPATH, XPATH_PREFIXO).text
			# STPOA_PREFIXO.append(text)
			# text = BROWSER.find_element(By.XPATH, XPATH_OPERADOR).text
			# STPOA_OPERADOR.append(text)
			# text = BROWSER.find_element(By.XPATH, XPATH_MOTIVO).text
			# STPOA_MOTIVO.append(text)
			# text = BROWSER.find_element(By.XPATH, XPATH_DATA).text
			# STPOA_DATA.append(text)
			# text = BROWSER.find_element(By.XPATH, XPATH_HORA).text
			# STPOA_HORA.append(text)
			# print(STPOA_LINHA)
			# print(STPOA_SENTIDO)
			# print(STPOA_PREFIXO)
			# print(STPOA_OPERADOR)
			# print(STPOA_MOTIVO)
			# print(STPOA_DATA)
			# print(STPOA_HORA)

	print(len(DESCRIÇÃO), len(PROTOCOLS), len(STPOA_LINHA), len(STPOA_PREFIXO), len(STPOA_MOTIVO), len(STPOA_HORA))


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
  # browser = start_firefox()
  # print(close_firefox(browser))
	# print(download_excel(2))
	get_protocols(fazer_magia())
	pass
