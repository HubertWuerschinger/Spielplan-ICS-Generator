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

data = []
total_cost = 0.0

if 'data' not in st.session_state:
    st.session_state.data = []

with st.form(key='inputs_form'):
    for i in range(len(st.session_state.data) + 1):
        cols = st.columns([2, 5, 4, 4, 4, 4])  # Anpassung der Spaltenbreiten
        with cols[0]:
            position = st.text_input(f"Position {i+1}", key=f'position_{i}')
        with cols[1]:
            name = st.text_input("Name", key=f'name_{i}')
        with cols[2]:
            arbeitszeit = st.number_input("Arbeitszeit (in Stunden)", min_value=0.0, value=0.0, step=0.5, key=f'arbeitszeit_{i}')
        with cols[3]:
            von = st.time_input("Von", key=f'von_{i}')
        with cols[4]:
            bis = st.time_input("Bis", key=f'bis_{i}')
        with cols[5]:
            kostenfaktor = st.number_input("Kostenfaktor (pro Stunde)", min_value=0.0, value=0.0, step=0.1, key=f'kostenfaktor_{i}')

        data.append([position, name, arbeitszeit, von, bis])
        total_cost += arbeitszeit * kostenfaktor

    add_row = st.form_submit_button(label='Weitere Zeile hinzufügen')
    create_document = st.form_submit_button(label='Word-Dokument erstellen und herunterladen')

if add_row:
    st.session_state.data = data

if create_document:
    df = pd.DataFrame(data, columns=['Position', 'Name', 'Arbeitszeit', 'Von', 'Bis'])
    template_path = 'template.docx'  # Pfad zur Vorlage
    doc_io = insert_text_in_template(df, total_cost, template_path)
    st.download_button(label="Word-Dokument herunterladen", data=doc_io, file_name="text_document.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
