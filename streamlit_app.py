import streamlit as st
import pandas as pd
import pdfplumber
import io

# Funktion, um Text aus PDF zu extrahieren
def extract_text_from_pdf(file):
    text = ''
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Funktion, um das Datum in datetime zu konvertieren
def convert_to_datetime(df, date_column):
    df[date_column] = pd.to_datetime(df[date_column])
    return df

# Streamlit App Start
st.title("Termine aus PDF extrahieren")

# PDF-Datei hochladen
uploaded_file = st.file_uploader("Lade eine PDF-Datei hoch", type=["pdf"])
if uploaded_file is not None:
    # Extrahiere Text aus der PDF
    extracted_text = extract_text_from_pdf(uploaded_file)

    # Hier müsste die Logik zur Extraktion der Termine aus dem Text implementiert werden
    # Für das Beispiel verwenden wir stattdessen einen Dummy-DataFrame
    dates_data = [
        {"Datum": "2024-01-01", "Ereignis": "Neujahr"},
        {"Datum": "2024-03-20", "Ereignis": "Frühlingsanfang"}
    ]
    df = pd.DataFrame(dates_data)

    # Konvertiere das Datum in datetime
    df = convert_to_datetime(df, "Datum")

    # Zeige eine editierbare Tabelle an
    edited_df = st.data_editor(df)

    if not edited_df.empty:
        # Stelle sicher, dass das Datum als datetime formatiert ist
        edited_df = convert_to_datetime(edited_df, "Datum")
        
        # Finde das Ereignis mit dem neuesten Datum
        favorite_event = edited_df.loc[edited_df["Datum"].idxmax()]["Ereignis"]
        st.markdown(f"Dein ausgewähltes Ereignis ist **{favorite_event}** 🎈")

# Streamlit App Ende
