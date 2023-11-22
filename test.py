from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from browser import (
	start_firefox,
	URL_FIND_PROTOCOL,
	URL_EPTC,
	XPATH_DETALHES_TRAMITES
)

protocol = '348090-23-17'

source = [
	'STPOA_LINHA',
	'STPOA_SENTIDO',
	'STPOA_PREFIXO',
	'STPOA_OPERADOR',
	'STPOA_MOTIVO',
	'STPOA_DATA',
	'STPOA_HORA'
]



	
BROWSER = start_firefox()
BROWSER.get(f'{URL_FIND_PROTOCOL}{protocol}')
BROWSER.find_element(By.XPATH, XPATH_DETALHES_TRAMITES).click()

URL_INFO_TRAMITE = f'{URL_EPTC}/Sistemas/156/fila/visualiza_info.php?protocolo={protocol}&seq_tramita=0&fase=0&cod_tramite=0'
BROWSER.get(URL_INFO_TRAMITE)

for i in source:
	td = BROWSER.find_element(By.XPATH, f"//td[text()='{i}']")
	text = td.find_element(By.XPATH, 'following-sibling::td').text
	print(text)