import streamlit as st
import cv2
import pytesseract
import pandas as pd
import numpy as np
from PIL import Image
import io

# OCR-Konfiguration
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract' # Pfad zu Tesseract-Executable anpassen

# Streamlit-Seitenlayout
st.title("Text- und Zahlen-Erkennung")

# Bild-Upload
uploaded_file = st.file_uploader("Bild hochladen", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Hochgeladenes Bild', use_column_width=True)
    
    # Bild in Text umwandeln
    text = pytesseract.image_to_string(image)
    st.write("Erkannter Text:")
    st.write(text)

    # Text in DataFrame umwandeln
    data = {'Text': text.split('\n')}
    df = pd.DataFrame(data)
    st.write(df)

    # Excel-Download
    towrite = io.BytesIO()
    df.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)
    st.download_button(label='Excel-Datei herunterladen', data=towrite, file_name='text_data.xlsx', mime='application/vnd.ms-excel')
