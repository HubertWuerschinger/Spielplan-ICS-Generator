import streamlit as st
import pandas as pd
import pytesseract
import cv2
import numpy as np
from PIL import Image
import io

# Konfiguriere pytesseract
pytesseract.pytesseract.tesseract_cmd = '/path/to/tesseract'

def extract_text_from_pdf(file):
    # Verwende Pillow, um das PDF in Bilder umzuwandeln
    images = convert_pdf_to_images(file)

    # Extrahiere Text aus jedem Bild
    text = ''
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

def convert_pdf_to_images(file):
    # Verwende OpenCV, um PDF-Seiten in Bilder umzuwandeln
    images = []
    file_stream = io.BytesIO(file.getvalue())
    pil_images = Image.open(file_stream)
    for i in range(pil_images.n_frames):
        pil_images.seek(i)
        image = np.array(pil_images)
        images.append(image)
    return images

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
