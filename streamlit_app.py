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
if 'data' not in st.session_state or not st.session_state.data:
    st.session_state.data = [{"Position": "", "Name": "", "Arbeitszeit": 0.0, "Von": datetime.time(0, 0), "Bis": datetime.time(0, 0), "Kostenfaktor": 0.0}]

# Funktion zum Hinzufügen einer neuen Zeile
def add_row():
    st.session_state.data.append({"Position": "", "Name": "", "Arbeitszeit": 0.0, "Von": datetime.time(0, 0), "Bis": datetime.time(0, 0), "Kostenfaktor": 0.0})

# Funktion zum Löschen einer Zeile
def delete_row(index):
    if len(st.session_state.data) > 1 and index < len(st.session_state.data):
        del st.session_state.data[index]

# Dynamische Anzeige von Eingabefeldern
for i, row in enumerate(st.session_state.data):
    cols = st.columns([1, 3, 2, 2, 2, 2, 1])
    with cols[0]:
        row["Position"] = st.text_input(f"Position {i+1}", value=row["Position"], key=f'position_{i}')
    with cols[1]:
        row["Name"] = st.text_input("Name", value=row["Name"], key=f'name_{i}')
    with cols[2]:
        row["Arbeitszeit"] = st.number_input("Arbeitszeit (in Stunden)", value=row["Arbeitszeit"], min_value=0.0, step=0.5, key=f'arbeitszeit_{i}')
    with cols[3]:
        row["Von"] = st.time_input("Von", value=row["Von"], key=f'von_{i}')
    with cols[4]:
        row["Bis"] = st.time_input("Bis", value=row["Bis"], key=f'bis_{i}')
    with cols[5]:
        row["Kostenfaktor"] = st.number_input("Kostenfaktor (pro Stunde)", value=row["Kostenfaktor"], min_value=0.0, step=0.1, key=f'kostenfaktor_{i}')
    with cols[6]:
        if st.button("Löschen", key=f'delete_{i}'):
            delete_row(i)

# Button zum Hinzufügen weiterer Zeilen
if st.button('Weitere Zeile hinzufügen'):
    add_row()

# Anzeige der Tabelle mit den aktuellen Daten
st.write("Aktuelle Eingaben:")
st.table(st.session_state.data)
