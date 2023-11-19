from PySimpleGUI import (
  Window, theme, WINDOW_CLOSED, Push, Button, Text, HSeparator)
  
from browser import start_firefox, close_firefox

SIZE_BUTTONS = (18, 1)

theme('Gray Gray Gray')
browser, LAYOUT = None, [
  [Text('Pegar reclamações da EPTC'), Push()],
  [Push(),
   Button('Abrir Firefox', size=SIZE_BUTTONS, disabled=False),
   Button('Fechar Firefox', size=SIZE_BUTTONS, disabled=True),
   Push()],
  [Text(text='', key='response firefox', visible=False)],
  [HSeparator()],
  [Text('Baixar as planilhas.'), Push()],
  [Button('LOTE 1'), Button('LOTE 2')],
]
WINDOW = Window('EPTC', LAYOUT)

while True:
  events, values = WINDOW.read()
  
  if events == 'Abrir Firefox':
    browser = start_firefox()
    WINDOW['Abrir Firefox'].update(disabled=True)
    WINDOW['Fechar Firefox'].update(disabled=False)
  
  if events == 'Fechar Firefox':
    response = close_firefox(browser)
    browser = None
    WINDOW['response firefox'].update(response)
    WINDOW['response firefox'].update(visible=True)
    WINDOW['Abrir Firefox'].update(disabled=False)
    WINDOW['Fechar Firefox'].update(disabled=True)
    


  if events == WINDOW_CLOSED:
    break

WINDOW.close()
