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

def add_row():
    st.session_state.data.append({'Position': '', 'Name': '', 'Arbeitszeit': 0.0, 'Von': datetime.time(0, 0), 'Bis': datetime.time(0, 0), 'Kostenfaktor': 0.0})
    st.session_state.dates.append(datetime.date.today())

def delete_row(index):
    if len(st.session_state.data) > 1:
        del st.session_state.data[index]
        del st.session_state.dates[index]

for i in range(len(st.session_state.data)):
    cols = st.columns([2, 1, 2, 2, 2, 2, 2, 1])
    with cols[0]:
        st.session_state.dates[i] = st.date_input("Datum", value=st.session_state.dates[i], key=f'date_{i}')
    with cols[1]:
        st.session_state.data[i]['Position'] = st.text_input("Position", value=st.session_state.data[i]['Position'], key=f'position_{i}')
    with cols[2]:
        st.session_state.data[i]['Name'] = st.text_input("Name", value=st.session_state.data[i]['Name'], key=f'name_{i}')
    with cols[3]:
        st.session_state.data[i]['Arbeitszeit'] = st.number_input("Arbeitszeit (in Stunden)", value=st.session_state.data[i]['Arbeitszeit'], min_value=0.0, step=0.5, key=f'arbeitszeit_{i}')
    with cols[4]:
        st.session_state.data[i]['Von'] = st.time_input("Von", value=st.session_state.data[i]['Von'], key=f'von_{i}')
    with cols[5]:
        st.session_state.data[i]['Bis'] = st.time_input("Bis", value=st.session_state.data[i]['Bis'], key=f'bis_{i}')
    with cols[6]:
        st.session_state.data[i]['Kostenfaktor'] = st.number_input("Kostenfaktor (pro Stunde)", value=st.session_state.data[i]['Kostenfaktor'], min_value=0.0, step=0.1, key=f'kostenfaktor_{i}')
    with cols[7]:
        if st.button("Löschen", key=f'delete_{i}'):
            delete_row(i)

if st.button('Weitere Zeile hinzufügen'):
    add_row()

# Anzeige der Tabelle mit den aktuellen Daten
st.write("Aktuelle Eingaben:")
current_data = []
for date, data in zip(st.session_state.dates, st.session_state.data):
    formatted_data = data.copy()
    formatted_data['Von'] = data['Von'].strftime('%H:%M')  # Formatieren als 'Stunden:Minuten'
    formatted_data['Bis'] = data['Bis'].strftime('%H:%M')  # Formatieren als 'Stunden:Minuten'
    current_data.append({'Datum': date, **formatted_data})

st.table(current_data)
