import streamlit as st
import pandas as pd
import pdfplumber
import io

def extract_text_from_pdf(file):
    text = ''
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Streamlit App Start
st.title("Termine aus PDF extrahieren")

uploaded_file = st.file_uploader("Lade eine PDF-Datei hoch", type=["pdf"])
if uploaded_file is not None:
    # Extrahiere Text aus der PDF
    extracted_text = extract_text_from_pdf(uploaded_file)

    # Implementiere hier die Logik zur Extraktion der Termine aus dem Text
    # und konvertiere sie in ein pandas DataFrame
    # Beispiel:
    dates_data = [
        {"Datum": "2024-01-01", "Ereignis": "Neujahr"},
        {"Datum": "2024-03-20", "Ereignis": "Frühlingsanfang"}
    ]
    df = pd.DataFrame(dates_data)

    # Zeige eine editierbare Tabelle an
    edited_df = st.data_editor(df)

    if not edited_df.empty:
        favorite_event = edited_df.loc[edited_df["Datum"].idxmax()]["Ereignis"]
        st.markdown(f"Dein ausgewähltes Ereignis ist **{favorite_event}** 🎈")

# Streamlit App Ende
