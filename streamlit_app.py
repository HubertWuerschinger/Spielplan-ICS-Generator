import streamlit as st
import pandas as pd
import pdfplumber
import io
from PIL import Image

# Funktion, um die erste Seite des PDFs als Bild umzuwandeln
def convert_pdf_page_to_image(file, page_number=0):
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[page_number]
        image = page.to_image()
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
    st.image(image, caption='PDF Vorschau', use_column_width=True)

    # Koordinaten für die Auswahl des Tabellenbereichs
    st.write("Gib die Koordinaten für den Tabellenbereich ein (x1, y1, x2, y2):")
    x1 = st.number_input("X1 Koordinate", min_value=0)
    y1 = st.number_input("Y1 Koordinate", min_value=0)
    x2 = st.number_input("X2 Koordinate", min_value=0)
    y2 = st.number_input("Y2 Koordinate", min_value=0)

    if st.button("Tabelle extrahieren"):
        # Extrahiere Tabelle aus dem ausgewählten Bereich
        table = extract_table_from_pdf_area(uploaded_file, (x1, y1, x2, y2))

        if table:
            # Wandle die extrahierte Tabelle in ein DataFrame um
            df = pd.DataFrame(table[1:], columns=table[0])

            # Zeige eine editierbare Tabelle an
            edited_df = st.data_editor(df)

            # Optionale Logik zur weiteren Verarbeitung der bearbeiteten Tabelle
            # ...

# Streamlit App Ende
