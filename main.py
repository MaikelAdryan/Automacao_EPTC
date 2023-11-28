# -*- coding: utf-8 -*-

from PySimpleGUI import (
  Window, theme, WINDOW_CLOSED, Push, Button, Text, HSep)
from browser import download_excel, get_informations_from_reclamation
from excel import read_excel

theme('Topanga')
browser, LAYOUT = None, [
  [Text('Baixar as planilhas.', font=(12))],
  [
    Push(),
    Button('LOTE 1', key='download lote 1', size=(7, 1), disabled=False),
    Button('LOTE 2', key='download lote 2', size=(7, 1), disabled=False),
    Button('AMBOS', key='download lotes', size=(7, 1), disabled=False),
    Push()
  ],
  [Text('', key='response donwload', visible=False)],

  [HSep()],

  [Text('Ler excels', font=(12)), Push()],
  [
    Push(),
    Button('LOTE 1', key='extract lote 1', size=(7, 1), disabled=False),
    Button('LOTE 2', key='extract lote 2', size=(7, 1), disabled=False),
    Button('EXTRAIR', key='extract relamations', size=(7, 1), disabled=False),
    Push()
  ],
  [Text('', key='response readed', visible=False)],

  [HSep()],
]
WINDOW = Window('EPTC', LAYOUT)

def add_response(key: str, new_text: str, visible: bool, color: str):
  WINDOW[key].update(visible=visible)
  WINDOW[key].update(text_color=color)
  WINDOW[key].update(new_text)


while True:
  events, values = WINDOW.read()

  if events == 'download lote 1':
    color, response = download_excel(1)
    add_response('response donwload', response, True, color)

  if events == 'download lote 2':
    color, response = download_excel(2)
    add_response('response donwload', response, True, color)

  if events == 'download lotes':
    for i in range(1, 3):
      color, response = download_excel(i)
      response = 'Excels LOTE 1 e 2 atualizados com sucesso!'
      add_response('response donwload', response, True, color)

  if events == 'extract lote 1':
    color, response = read_excel('LOTE_1.xls')
    add_response('response readed', response, True, color)

  if events == 'extract lote 2':
    color, response = read_excel('LOTE_2.xls')
    add_response('response readed', response, True, color)

  if events == 'extract relamations':
    get_informations_from_reclamation()

  if events == WINDOW_CLOSED:
    break

WINDOW.close()
