# -*- coding: utf-8 -*-

from browser import download_excel, get_informations_from_reclamation_and_insert_to_db
from excel import read_excel

download_excel()
contains_lote_1 = read_excel('LOTE_1.xls')
if contains_lote_1:
	get_informations_from_reclamation_and_insert_to_db()
contains_lote_2 = read_excel('LOTE_2.xls')
if contains_lote_2:
	get_informations_from_reclamation_and_insert_to_db()
