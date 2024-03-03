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
    st.session_state.data = [{"Position": "", "Name": "", "Arbeitszeit": 0.0, "Von": datetime.time(0, 0), "Bis": datetime.time(0, 0), "Kostenfaktor": 0.0}]

# Funktion zum Hinzufügen einer neuen Zeile
def add_row():
    st.session_state.data.append({"Position": "", "Name": "", "Arbeitszeit": 0.0, "Von": datetime.time(0, 0), "Bis": datetime.time(0, 0), "Kostenfaktor": 0.0})

# Einfache Anzeige der ersten Zeile von Eingabefeldern
position = st.text_input("Position", key='position_0')
name = st.text_input("Name", key='name_0')
arbeitszeit = st.number_input("Arbeitszeit (in Stunden)", min_value=0.0, value=0.0, step=0.5, key='arbeitszeit_0')
von = st.time_input("Von", key='von_0')
bis = st.time_input("Bis", key='bis_0')
kostenfaktor = st.number_input("Kostenfaktor (pro Stunde)", min_value=0.0, value=0.0, step=0.1, key='kostenfaktor_0')

# Button zum Hinzufügen weiterer Zeilen
if st.button('Weitere Zeile hinzufügen'):
    add_row()

# Anzeige der Tabelle mit den aktuellen Daten
st.write("Aktuelle Eingaben:")
st.table(st.session_state.data)
