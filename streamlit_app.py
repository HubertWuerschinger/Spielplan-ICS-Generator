from __future__ import annotations
import streamlit as st
import streamlit_image_crop
from streamlit_image_crop import image_crop, Crop
import pdfplumber
import io
from PIL import Image

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

def main() -> None:
    st.title("PDF Tabellenbereich extrahieren mit Image Crop")

    # PDF-Datei hochladen
    uploaded_file = st.file_uploader("Lade eine PDF-Datei hoch", type=["pdf"])
    if uploaded_file is not None:
        # Konvertiere die erste Seite des PDFs in ein Bild
        image = convert_pdf_page_to_image(uploaded_file)
        if image:
            # Konvertiere das Bild in ein Format, das von streamlit_image_crop akzeptiert wird
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            bytes_image = buffered.getvalue()

            # Parameter für das Zuschneiden
            fixed_aspect_ratio = st.sidebar.checkbox("Fixed aspect cropping", value=False)
            aspect_ratio = None if not fixed_aspect_ratio else st.sidebar.slider("Aspect ratio", value=1.0, min_value=0.2, max_value=5.0, step=0.2)
            min_width = st.sidebar.slider("Minimum width", value=0, min_value=0, max_value=200)
            max_width = st.sidebar.slider("Maximum width", value=1000, min_value=0, max_value=1000)
            min_height = st.sidebar.slider("Minimum height", value=0, min_value=0, max_value=200)
            max_height = st.sidebar.slider("Maximum height", value=1000, min_value=0, max_value=1000)
            rule_of_thirds = st.sidebar.checkbox("Rule of Thirds", value=False)
            circular_crop = st.sidebar.checkbox("Circular Crop", value=False)

            # Zuschneiden des Bildes
            col_left, col_right = st.columns(2)
            with col_left:
                image_cropped = image_crop(
                    bytes_image,
                    crop=Crop(aspect=aspect_ratio),
                    min_width=min_width,
                    min_height=min_height,
                    max_width=max_width,
                    max_height=max_height,
                    rule_of_thirds=rule_of_thirds,
                    circular_crop=circular_crop,
                )

            if image_cropped is not None:
                # Verarbeite den zugeschnittenen Bereich
                with col_right:
                    st.image(image_cropped, use_column_width=True)

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

main()
