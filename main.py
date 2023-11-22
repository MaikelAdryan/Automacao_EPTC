from PySimpleGUI import (
  Window, theme, WINDOW_CLOSED, Push, Button, Text, HSep, theme_previewer)
from browser import start_firefox, close_firefox, download_excel
from excel import move_excel

theme('LightBrown1')
browser, LAYOUT = None, [
  [Text('Baixar as planilhas.', font=(12)), Push()],
  [
    Button('LOTE 1', size=(7, 1), disabled=False),
    Button('LOTE 2', size=(7, 1), disabled=False),
    Button('AMBOS', size=(7, 1), disabled=False)
  ],
  [ Text('', key='response excel', visible=False)],
  [HSep()],
  [Text('Pegar reclamações da EPTC'), Push()],
  [
    Push(),
    Button('Abrir Firefox', size=(18, 1), disabled=False),
    Button('Fechar Firefox', size=(18, 1), disabled=True),
    Push()
  ],
  [Text(text='', key='response firefox', visible=False)],
  [HSep()]
]
WINDOW = Window('EPTC', LAYOUT)

def add_response(key: str, text: str, visible: bool, color: text_color):
	WINDOW[key].update(visible=visible)
	WINDOW[key].update(text_color=color)
	WINDOW[key].update(text)


while True:
	events, values = WINDOW.read()

	if events == 'Abrir Firefox':
		browser = start_firefox()
		WINDOW['Abrir Firefox'].update(disabled=True)
		WINDOW['Fechar Firefox'].update(disabled=False)
		WINDOW['LOTE 1'].update(disabled=False)
		WINDOW['LOTE 2'].update(disabled=False)

	if events == 'Fechar Firefox':
		response = close_firefox(browser)
		browser = None
		WINDOW['response firefox'].update(response)
		WINDOW['response firefox'].update(visible=True)
		WINDOW['Abrir Firefox'].update(disabled=False)
		WINDOW['Fechar Firefox'].update(disabled=True)
		WINDOW['LOTE 1'].update(disabled=False)
		WINDOW['LOTE 2'].update(disabled=False)

	if events == 'LOTE 1':
		download_excel(1)
		color, response = move_excel('LOTE_1')
		add_response('response excel', response, True, color)
		
	if events == 'LOTE 2':
		download_excel(2)
		color, response = move_excel('LOTE_2')
		add_response('response excel', response, True, color)

	if events == 'AMBOS':
		for i in range(1, 3):
			download_excel(i)
			color, response = move_excel(f'LOTE_{i}')
			add_response('response excel', response, True, color)

	if events == WINDOW_CLOSED:
		break

WINDOW.close()
