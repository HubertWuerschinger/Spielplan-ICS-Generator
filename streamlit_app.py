import streamlit as st
import pdfplumber
import io
import numpy as np
from PIL import Image
from streamlit_cropperjs import st_cropperjs

# Funktion, um die erste Seite des PDFs als Bild umzuwandeln
def convert_pdf_page_to_image(file, page_number=0):
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[page_number]
        image = page.to_image().original
        return image

# Funktion zum Extrahieren eines Tabellenbereichs aus einer PDF
def extract_table_from_pdf_area(file, bbox):
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]
        table = page.extract_table({"bbox": bbox})
        return table

# Streamlit App Start
st.title("PDF Tabellenbereich extrahieren mit CropperJS")

# PDF-Datei hochladen
uploaded_file = st.file_uploader("Lade eine PDF-Datei hoch", type=["pdf"])
if uploaded_file is not None:
    # Konvertiere die erste Seite des PDFs in ein Bild
    image = convert_pdf_page_to_image(uploaded_file)
    if image:
        # Konvertiere das Bild in ein Format, das von streamlit_cropperjs akzeptiert wird
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        pic = buffered.getvalue()

        # Verwende streamlit_cropperjs zum Zuschneiden
        cropped_pic = st_cropperjs(pic=pic, btn_text="Detect!", key="foo")
        if cropped_pic:
            # Verarbeite das zugeschnittene Bild für die Datenextraktion
            st.image(cropped_pic, output_format="PNG")
            st.download_button(
                "Download", cropped_pic, file_name="output.png", mime="image/png"
            )

            # Berechne die Koordinaten des zugeschnittenen Bereichs für die Datenextraktion
            # Hinweis: Implementiere die Logik zur Berechnung der bbox aus dem zugeschnittenen Bild
            # bbox = ...

            # Extrahiere Tabelle aus dem ausgewählten Bereich
            # table = extract_table_from_pdf_area(uploaded_file, bbox)
            # if table:
                # Wandle die extrahierte Tabelle in ein DataFrame um
                # df = pd.DataFrame(table[1:], columns=table[0])
                # Zeige die bearbeitete Tabelle an
                # st.dataframe(df)

# Streamlit App Ende
