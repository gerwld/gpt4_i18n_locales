"""Gets 2 html documents,then finds the keys data-i18n which wasn't used in DOCUMENT_2."""
"""Бере 2 хтмл документи, після знаходить ключі data-i18n які не використвуються в DOCUMENT_2."""
import os
import time
import random
from global_context import C_RED
from bs4 import BeautifulSoup

DOCUMENT_1 = 'doc1.html' #source doc
DOCUMENT_2 = 'doc2.html' #new doc, that contains only few data-i18n from doc1

def read_data_i18n(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        # Find all elements with the data-i18n attribute
        elements = soup.find_all(attrs={'data-i18n': True})
        # Extract values of the data-i18n attribute into an array
        values_array = [element['data-i18n'] for element in elements]
    return values_array

doc1attr_values = read_data_i18n(DOCUMENT_1)
doc2attr_values = read_data_i18n(DOCUMENT_2)
unused_values = [v for v in doc1attr_values if v not in doc2attr_values]
print(f'{C_RED}DOC1 attr count: {len(doc1attr_values)}, DOC2: {len(doc2attr_values)}{C_RED.OFF}')
print(f"Unused ({len(unused_values)}): {unused_values}")
