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

def create_word_document(text, template_path, save_path):
    doc = Document(template_path)
    doc.add_paragraph(text)
    doc.save(save_path)

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

    # Bereinigen Sie den Text von nicht-druckbaren Zeichen
    cleaned_text = remove_non_printable_chars(text)

    # Textbearbeitungsfeld
    st.write("Erkannter Text (bearbeitbar):")
    edited_text = st.text_area("", cleaned_text, height=300)

    # Erstellen eines Word-Dokuments
    if st.button('In Word-Dokument umwandeln'):
        template_path = 'pfad/zu/Ihrer/template.docx'  # Pfad zur Vorlage
        save_path = 'pfad/wo/sie/speichern/möchten/output.docx'
        create_word_document(edited_text, template_path, save_path)
        st.success('Word-Dokument erfolgreich erstellt!')

    # Speichern als Excel-Datei
    if st.button('In Excel-Datei umwandeln'):
        data = {'Text': edited_text.split('\n')}
        df = pd.DataFrame(data)

        towrite = io.BytesIO()
        df.to_excel(towrite, index=False, header=True)
        towrite.seek(0)
        st.download_button(label='Excel-Datei herunterladen', data=towrite, file_name='text_data.xlsx', mime='application/vnd.ms-excel')
