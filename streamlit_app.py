import streamlit as st
import pandas as pd
from docx import Document
import io
import datetime

# Setze das Seitenlayout auf breit
st.set_page_config(layout="wide")

st.title("Arbeitszeiten und Kostenberechnung")

# Initialisiere Session State für die Datenspeicherung
if 'data' not in st.session_state:
    st.session_state.data = [{'Position': '', 'Name': '', 'Arbeitszeit': 0.0, 'Von': datetime.time(0, 0), 'Bis': datetime.time(0, 0), 'Kostenfaktor': 0.0}]

if 'dates' not in st.session_state:
    st.session_state.dates = [datetime.date.today() for _ in st.session_state.data]

# Funktion zum Hinzufügen einer neuen Zeile
def add_row():
    st.session_state.data.append({'Position': '', 'Name': '', 'Arbeitszeit': 0.0, 'Von': datetime.time(0, 0), 'Bis': datetime.time(0, 0), 'Kostenfaktor': 0.0})
    st.session_state.dates.append(datetime.date.today())

# Funktion zum Löschen einer Zeile
def delete_row(index):
    if len(st.session_state.data) > 1:
        del st.session_state.data[index]
        del st.session_state.dates[index]

# Dynamische Anzeige von Eingabefeldern
for i in range(len(st.session_state.data)):
    cols = st.columns([2, 1, 3, 2, 2, 2, 2, 1])
    with cols[0]:
        st.session_state.dates[i] = st.date_input("Datum", value=st.session_state.dates[i], key=f'date_{i}')
    with cols[1]:
        st.session_state.data[i]['Position'] = st.text_input("Position", value=st.session_state.data[i]['Position'], key=f'position_{i}')
    # ... Fortsetzung für andere Felder ...
    with cols[7]:
        if st.button("Löschen", key=f'delete_{i}'):
            delete_row(i)

if st.button('Weitere Zeile hinzufügen'):
    add_row()

# Anzeige der Tabelle mit den aktuellen Daten
st.write("Aktuelle Eingaben:")
current_data = [{'Datum': date, **data} for date, data in zip(st.session_state.dates, st.session_state.data)]
st.table(current_data)
