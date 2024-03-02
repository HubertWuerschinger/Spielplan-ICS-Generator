import streamlit as st
import pytesseract
import pandas as pd
from PIL import Image
import io
import re



# OCR-Konfiguration
# Hinweis: Ändern Sie den Pfad entsprechend Ihrer Tesseract-Installation
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Für Linux/Mac
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Für Windows

# Streamlit-Seitenlayout
st.title("Text- und Zahlen-Erkennung")

# Bild-Upload
uploaded_file = st.file_uploader("Bild hochladen", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Hochgeladenes Bild', use_column_width=True)
    
    # Bild in Text umwandeln
    text = pytesseract.image_to_string(image)
    cleaned_text = remove_non_printable_chars(text)

    st.write("Erkannter Text:")
    st.write(cleaned_text)

    # Text in DataFrame umwandeln
    def remove_illegal_chars_for_excel(text):
        # Entfernt alle Zeichen, die in Excel-Tabellen nicht zulässig sind
        # Hier werden alle Zeichen außer druckbaren ASCII-Zeichen entfernt
        return re.sub(r'[^\x20-\x7E]', '', text)
    #data = {'Text': cleaned_text.split('\n')}
    
    

    # Angenommen, 'text' enthält Ihren OCR-erfassten Text
    cleaned_text = remove_illegal_chars_for_excel(text)

    # Erstellen Sie die DataFrame mit dem bereinigten Text
    data = {'Text': cleaned_text.split('\n')}
    df = pd.DataFrame(data)
    st.write(df)


    
    # Excel-Download
    towrite = io.BytesIO()
    df.to_excel(towrite, index=False, header=True)
    towrite.seek(0)
    st.download_button(label='Excel-Datei herunterladen', data=towrite, file_name='text_data.xlsx', mime='application/vnd.ms-excel')
