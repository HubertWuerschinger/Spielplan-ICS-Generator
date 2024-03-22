import streamlit as st
from PIL import Image
import io
import pdfplumber

# Funktion, um die erste Seite des PDFs als Bild umzuwandeln
def convert_pdf_page_to_image(file, page_number=0):
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[page_number]
        image = page.to_image().original
        return image

def main():
    st.title("Bereich aus PDF extrahieren durch manuelle Koordinateneingabe")

    # PDF-Datei hochladen
    uploaded_file = st.file_uploader("Lade eine PDF-Datei hoch", type=["pdf"])
    if uploaded_file is not None:
        image = convert_pdf_page_to_image(uploaded_file)
        st.image(image, caption='PDF Vorschau', use_column_width=True)

        # Eingabe der Koordinaten
        st.sidebar.header("Koordinaten für den Bildbereich")
        x1 = st.sidebar.number_input("X1 Koordinate", min_value=0, max_value=image.width, value=0)
        y1 = st.sidebar.number_input("Y1 Koordinate", min_value=0, max_value=image.height, value=0)
        x2 = st.sidebar.number_input("X2 Koordinate", min_value=0, max_value=image.width, value=image.width)
        y2 = st.sidebar.number_input("Y2 Koordinate", min_value=0, max_value=image.height, value=image.height)

        # Zeige den ausgewählten Bereich, wenn die Koordinaten gegeben sind
        if st.button("Bereich anzeigen"):
            cropped_image = image.crop((x1, y1, x2, y2))
            st.image(cropped_image, caption="Ausgewählter Bereich")

            # Hier können weitere Verarbeitungsschritte folgen, 
            # z.B. Extraktion von Daten aus dem Bildbereich.

main()
