import streamlit as st
import pandas as pd
from docx import Document
import io

import datetime




# Setze das Seitenlayout auf breit
st.set_page_config(layout="wide")

def insert_text_in_template(df, total_cost, template_path):
    doc = Document(template_path)
    if len(doc.paragraphs) >= 8:
        para = doc.paragraphs[7]
        para.add_run("\n\nTabelle:\n")
        for index, row in df.iterrows():
            para.add_run(f"{row['Position']} | {row['Name']} | {row['Arbeitszeit']} | {row['Von']} | {row['Bis']}\n")
        para.add_run(f"\nGesamtkosten: {total_cost}")
    else:
        doc.add_paragraph("Tabelle:")
        for index, row in df.iterrows():
            doc.add_paragraph(f"{row['Position']} | {row['Name']} | {row['Arbeitszeit']} | {row['Von']} | {row['Bis']}")
        doc.add_paragraph(f"Gesamtkosten: {total_cost}")

    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
return doc_io

st.title("Arbeitszeiten und Kostenberechnung")

if 'data' not in st.session_state:
    st.session_state.data = []

# Funktion zum Hinzufügen einer neuen Zeile
def add_row():
    st.session_state.data.append({
        "Position": "", 
        "Name": "", 
        "Arbeitszeit": 0.0, 
        "Von": datetime.time(0, 0),  # Initialisiere mit Mitternacht
        "Bis": datetime.time(0, 0),  # Initialisiere mit Mitternacht
        "Kostenfaktor": 0.0
    })
# Funktion zum Löschen einer Zeile
def delete_row(index):
    if index < len(st.session_state.data):
        del st.session_state.data[index]

# Zeigt die dynamische Tabelle an
def display_table():
    new_data = []
    for i, row in enumerate(st.session_state.data):
        cols = st.columns([1, 3, 2, 2, 2, 2, 1])
        with cols[0]:
            position = st.text_input(f"Position {i+1}", value=row["Position"], key=f'position_{i}')
        with cols[1]:
            name = st.text_input("Name", value=row["Name"], key=f'name_{i}')
        with cols[2]:
            arbeitszeit = st.number_input("Arbeitszeit (in Stunden)", value=row["Arbeitszeit"], min_value=0.0, step=0.5, key=f'arbeitszeit_{i}')
        with cols[3]:
            row["Von"] = st.time_input("Von", value=row["Von"], key=f'von_{i}')
        with cols[4]:
            row["Bis"] = st.time_input("Bis", value=row["Bis"], key=f'bis_{i}')
        with cols[5]:
            kostenfaktor = st.number_input("Kostenfaktor (pro Stunde)", value=row["Kostenfaktor"], min_value=0.0, step=0.1, key=f'kostenfaktor_{i}')
        new_data.append({"Position": position, "Name": name, "Arbeitszeit": arbeitszeit, "Von": von, "Bis": bis, "Kostenfaktor": kostenfaktor})
        with cols[6]:
            if st.button("Löschen", key=f'delete_{i}'):
                delete_row(i)

    st.session_state.data = new_data

# Anzeige und Bearbeitung der Tabelle
display_table()

if st.button('Weitere Zeile hinzufügen'):
    add_row()

# Berechnung der Gesamtkosten
total_cost = sum(row["Arbeitszeit"] * row["Kostenfaktor"] for row in st.session_state.data)

# Erstellen und Herunterladen des Word-Dokuments
if st.button('Word-Dokument erstellen und herunterladen'):
    df = pd.DataFrame(st.session_state.data)
    template_path = 'template.docx'  # Pfad zur Vorlage
    doc_io = insert_text_in_template(df, total_cost, template_path)
    st.download_button(label="Word-Dokument herunterladen", data=doc_io, file_name="text_document.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

# Anzeige der Tabelle
st.write("Aktuelle Eingaben:")
st.table(st.session_state.data)
