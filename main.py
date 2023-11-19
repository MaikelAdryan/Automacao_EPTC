import PySimpleGUI as sg
from browser import start_firefox, close_firefox

browser = None

sg.theme('Python')
LAYOUT = [
  # [sg.Text('')],
  [sg.Push(),
   sg.Button('Abrir Firefox', disabled=False),
   sg.Button('Fechar Firefox', disabled=False),
   sg.Push()],
  [sg.Text(text='', key='response firefox', visible=False)],
  [sg.HSeparator()]
]
WINDOW = sg.Window('Automação EPTC', LAYOUT)

while True:
  events, values = WINDOW.read()
  
  if events == 'Abrir Firefox':
    browser = start_firefox()
    WINDOW['Fechar Firefox'].update(disabled=False)
    
  
  if events == 'Fechar Firefox':
    response = close_firefox(browser)
    print(response)
    WINDOW['response firefox'].update(response)
    WINDOW['response firefox'].update(visible=True)


  if events == sg.WINDOW_CLOSED:
    break

WINDOW.close()
