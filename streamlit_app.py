import streamlit as st
import pdfplumber
import io
import numpy as np
from streamlit_cropper import st_cropper
from PIL import Image

st.set_option('deprecation.showfileUploaderEncoding', False)

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
st.title("PDF Tabellenbereich extrahieren")

# PDF-Datei hochladen
uploaded_file = st.file_uploader("Lade eine PDF-Datei hoch", type=["pdf"])
if uploaded_file is not None:
    # Zeige die erste Seite des PDFs als Bild an
    image = convert_pdf_page_to_image(uploaded_file)
    if image:
        # Konvertiere das Bild in ein unterstütztes Format
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img = Image.open(buffered)

        # Cropper Optionen
        realtime_update = st.sidebar.checkbox("Update in Real Time", value=True)
        box_color = st.sidebar.color_picker("Box Color", value='#0000FF')
        stroke_width = st.sidebar.number_input("Box Thickness", value=3, step=1)
        aspect_ratio = None  # Freie Auswahl des Bereichs

        # Verwende Cropper, um den Bereich zu wählen
        cropped_area = st_cropper(
            img, 
            realtime_update=realtime_update, 
            box_color=box_color, 
            aspect_ratio=aspect_ratio, 
            return_type='box', 
            stroke_width=stroke_width
        )

        if cropped_area and st.button("Tabelle extrahieren"):
            # Extrahiere Tabelle aus dem ausgewählten Bereich
            table = extract_table_from_pdf_area(uploaded_file, cropped_area)

            if table:
                # Wandle die extrahierte Tabelle in ein DataFrame um
                df = pd.DataFrame(table[1:], columns=table[0])

                # Zeige die bearbeitete Tabelle an
                st.dataframe(df)
