import streamlit as st
import pandas as pd
from docx import Document
import io
import datetime

# Setze das Seitenlayout auf breit
st.set_page_config(layout="wide")

# Titel der Anwendung
st.title("Arbeitszeiten und Kostenberechnung")

# Initialisiere Session State für die Datenspeicherung, falls noch nicht vorhanden
if 'data' not in st.session_state:
    st.session_state['data'] = [{'Datum': datetime.date.today(), 'Position': '', 'Name': '', 'Arbeitszeit': 0.0, 'Von': datetime.time(0, 0), 'Bis': datetime.time(0, 0), 'Kostenfaktor': 0.0}]

# Funktion zum Hinzufügen einer neuen Zeile
def add_row():
    st.session_state['data'].append({'Datum': datetime.date.today(), 'Position': '', 'Name': '', 'Arbeitszeit': 0.0, 'Von': datetime.time(0, 0), 'Bis': datetime.time(0, 0), 'Kostenfaktor': 0.0})

# Funktion zum Löschen einer Zeile
def delete_row(index):
    if len(st.session_state['data']) > 1:
        st.session_state['data'].pop(index)

# Dynamische Anzeige von Eingabefeldern
for i, row in enumerate(st.session_state['data']):
    cols = st.columns([2, 1, 3, 2, 2, 2, 2, 1])
    with cols[0]:
        row['Datum'] = st.date_input("Datum", value=row['Datum'], key=f'date_{i}')
    with cols[1]:
        row['Position'] = st.text_input("Position", value=row['Position'], key=f'position_{i}')
    # ... und so weiter für die anderen Felder

# Button zum Hinzufügen weiterer Zeilen
if st.button('Weitere Zeile hinzufügen'):
    add_row()

# Anzeige der Tabelle mit den aktuellen Daten
st.write("Aktuelle Eingaben:")
st.table(st.session_state['data'])
