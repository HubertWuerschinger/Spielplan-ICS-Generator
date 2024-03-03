import streamlit as st
import pytesseract
import pandas as pd
from PIL import Image
import io
import re
from docx import Document

# Funktion zur Bereinigung von nicht-druckbaren Zeichen
def remove_non_printable_chars(text):
    return re.sub(r'[^\x20-\x7E]', '', text)

def insert_text_in_template(text, df, total_cost, template_path):
    doc = Document(template_path)
    # Füge den bearbeiteten Text und die Tabelle in das Dokument ein
    if len(doc.paragraphs) >= 8:
        para = doc.paragraphs[7]
        para.add_run(text)
        para.add_run("\n\nTabelle:\n")
        for index, row in df.iterrows():
            para.add_run(f"{row['Position']} | {row['Name']} | {row['Arbeitszeit']} | {row['Von']} | {row['Bis']}\n")
        para.add_run(f"\nGesamtkosten: {total_cost}")
    else:
        doc.add_paragraph(text)
        doc.add_paragraph("Tabelle:")
        for index, row in df.iterrows():
            doc.add_paragraph(f"{row['Position']} | {row['Name']} | {row['Arbeitszeit']} | {row['Von']} | {row['Bis']}")
        doc.add_paragraph(f"Gesamtkosten: {total_cost}")

    # Speichere das Dokument im Speicher
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    return doc_io

# OCR-Konfiguration
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Für Linux/Mac

# Streamlit-Seitenlayout
st.title("Text- und Zahlen-Erkennung mit Kostenermittlung")

# Bild-Upload
uploaded_file = st.file_uploader("Bild hochladen", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Hochgeladenes Bild', use_column_width=True)
    
    # Bild in Text umwandeln
    text = pytesseract.image_to_string(image)

    # Bereinigen Sie den Text von nicht-druckbaren Zeichen
    cleaned_text = remove_non_printable_chars(text)

    # Textbearbeitungsfeld
    st.write("Erkannter Text (bearbeitbar):")
    edited_text = st.text_area("", cleaned_text, height=300)

    # Tabelle für Benutzereingaben
    st.write("Geben Sie Daten in die Tabelle ein:")
    with st.form(key='my_form'):
        position = st.text_input("Position")
        name = st.text_input("Name")
        arbeitszeit = st.number_input("Arbeitszeit (in Stunden)", min_value=0.0, value=0.0, step=0.5)
        von = st.time_input("Von")
        bis = st.time_input("Bis")
        kostenfaktor = st.number_input("Kostenfaktor (pro Stunde)", min_value=0.0, value=0.0, step=0.1)
        submit_button = st.form_submit_button(label='Berechnen und hinzufügen')

    if submit_button:
        # Berechnung der Gesamtkosten
        total_cost = arbeitszeit * kostenfaktor

        # Erstellung der Tabelle
        data = {'Position': [position], 'Name': [name], 'Arbeitszeit': [arbeitszeit], 'Von': [von], 'Bis': [bis]}
        df = pd.DataFrame(data)

        # Erstellen und Herunterladen des Word-Dokuments
        template_path = 'template.docx'  # Pfad zur Vorlage
        doc_io = insert_text_in_template(edited_text, df, total_cost, template_path)
        st.download_button(label="Word-Dokument herunterladen", data=doc_io, file_name="text_document.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
