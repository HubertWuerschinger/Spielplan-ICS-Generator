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

# Funktion zum Umwandeln der extrahierten Tabellen in DataFrames
def tables_to_dataframes(tables):
    dataframes = []
    for table in tables:
        df = pd.DataFrame(table[1:], columns=table[0])
        dataframes.append(df)
    return dataframes

# Streamlit App Start
st.title("Tabellen aus PDF extrahieren und bearbeiten")

# PDF-Datei hochladen
uploaded_file = st.file_uploader("Lade eine PDF-Datei hoch", type=["pdf"])
if uploaded_file is not None:
    # Extrahiere Tabellen aus der PDF
    tables = extract_tables_from_pdf(uploaded_file)

    if tables:
        # Wandle die extrahierten Tabellen in DataFrames um
        dataframes = tables_to_dataframes(tables)

        # Wähle eine Tabelle zum Anzeigen und Bearbeiten aus
        selected_table_index = st.selectbox("Wähle eine Tabelle aus", range(len(dataframes)))
        selected_table = dataframes[selected_table_index]

        # Zeige eine editierbare Tabelle an
        edited_df = st.data_editor(selected_table)

        # Optionale Logik zur weiteren Verarbeitung der bearbeiteten Tabelle
        # ...

# Streamlit App Ende
