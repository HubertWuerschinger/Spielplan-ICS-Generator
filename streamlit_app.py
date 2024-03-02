import streamlit as st
import pytesseract
import pandas as pd
from PIL import Image
import io
import re

# Funktion zur Bereinigung von nicht-druckbaren Zeichen
def remove_non_printable_chars(text):
    # Entfernt alle Zeichen, die in Excel-Tabellen nicht zulässig sind
    # Hier werden alle Zeichen außer druckbaren ASCII-Zeichen entfernt
    return re.sub(r'[^\x20-\x7E]', '', text)

# OCR-Konfiguration
# Hinweis: Ändern Sie den Pfad entsprechend Ihrer Tesseract-Installation
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Für Linux/Mac
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Für Windows

# Streamlit-Seitenlayout
st.title("Text- und Zahlen-Erkennung")

# Bild-Upload
uploaded_file = st.file_uploader("Bild hochladen", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
# Bild in Text umwandeln
    text = pytesseract.image_to_string(image)

    # Bereinigen Sie den Text von nicht-druckbaren Zeichen
    cleaned_text = remove_non_printable_chars(text)

    st.write("Erkannter Text:")
    st.write(cleaned_text)

    # Text in DataFrame umwandeln
    data = {'Text': cleaned_text.split('\n')}
    df = pd.DataFrame(data)
    st.write(df)

    # Excel-Download
    towrite = io.BytesIO()
    df.to_excel(towrite, index=False, header=True)
    towrite.seek(0)
    st.download_button(label='Excel-Datei herunterladen', data=towrite, file_name='text_data.xlsx', mime='application/vnd.ms-excel')
