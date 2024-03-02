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

def insert_text_in_template(text, template_path):
    doc = Document(template_path)
    # Gehe zur gewünschten Zeile (Zeile 8) und füge Text ein
    # Beachten Sie, dass Python bei 0 zu zählen beginnt, daher ist Zeile 8 in der Liste die 7. Position
    if len(doc.paragraphs) >= 8:
        para = doc.paragraphs[7]
        para.add_run(text)
    else:
        # Falls weniger als 8 Zeilen vorhanden sind, wird der Text am Ende hinzugefügt
        doc.add_paragraph(text)

    # Speichere das Dokument im Speicher
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    return doc_io


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


 # Erstellen und Herunterladen des Word-Dokuments
    if st.button('Word-Dokument erstellen und herunterladen'):
        template_path = 'template.docx'  # Pfad zur Vorlage
        doc_io = insert_text_in_template(edited_text, template_path)
        st.download_button(label="Word-Dokument herunterladen", data=doc_io, file_name="text_document.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    # Speichern als Excel-Datei
    if st.button('Excel-Datei erstellen und herunterladen'):
        data = {'Text': edited_text.split('\n')}
        df = pd.DataFrame(data)

        towrite = io.BytesIO()
        df.to_excel(towrite, index=False, header=True)
        towrite.seek(0)
        st.download_button(label='Excel-Datei herunterladen', data=towrite, file_name='text_data.xlsx', mime='application/vnd.ms-excel')
