import streamlit as st
import pandas as pd
import pdfplumber
import io

# Funktion zum Extrahieren von Tabellen aus einer PDF
def extract_tables_from_pdf(file):
    all_tables = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            # Extrahiere Tabellen von dieser Seite
            tables = page.extract_tables()
            for table in tables:
                all_tables.append(table)
    return all_tables

# Streamlit App Start
st.title("Tabellen aus PDF extrahieren und bearbeiten")

# PDF-Datei hochladen
uploaded_file = st.file_uploader("Lade eine PDF-Datei hoch", type=["pdf"])
if uploaded_file is not None:
    # Extrahiere Tabellen aus der PDF
    tables = extract_tables_from_pdf(uploaded_file)

    if tables:
        # Wandle die erste Tabelle in ein DataFrame um
        df = pd.DataFrame(tables[0][1:], columns=tables[0][0])

        # Zeige eine editierbare Tabelle an
        edited_df = st.data_editor(df)

        # Optionale Logik zur weiteren Verarbeitung der bearbeiteten Tabelle
        # ...

# Streamlit App Ende
