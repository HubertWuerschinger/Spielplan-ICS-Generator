import streamlit as st
import pandas as pd
from docx import Document
import io

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
    st.session_state.data.append({"Position": "", "Name": "", "Arbeitszeit": 0.0, "Von": "00:00", "Bis": "00:00", "Kostenfaktor": 0.0})

# Funktion zum Löschen einer Zeile
def delete_row(index):
    if index < len(st.session_state.data):
        del st.session_state.data[index]

# Anzeige und Bearbeitung der Tabelle
for i in range(len(st.session_state.data)):
    cols = st.columns([6, 8, 8, 8, 8, 8, 8])
    with cols[0]:
        st.session_state.data[i]["Position"] = st.text_input(f"Position {i+1}", key=f'position_{i}')
    with cols[1]:
        st.session_state.data[i]["Name"] = st.text_input("Name", key=f'name_{i}')
    with cols[2]:
        st.session_state.data[i]["Arbeitszeit"] = st.number_input("Arbeitszeit (in Stunden)", min_value=0.0, value=0.0, step=0.5, key=f'arbeitszeit_{i}')
    with cols[3]:
        st.session_state.data[i]["Von"] = st.time_input("Von", key=f'von_{i}')
    with cols[4]:
        st.session_state.data[i]["Bis"] = st.time_input("Bis", key=f'bis_{i}')
    with cols[5]:
        st.session_state.data[i]["Kostenfaktor"] = st.number_input("Kostenfaktor (pro Stunde)", min_value=0.0, value=0.0, step=0.1, key=f'kostenfaktor_{i}')
    with cols[6]:
        st.button("Löschen", key=f'delete_{i}', on_click=delete_row, args=(i,))

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
