import streamlit as st
import pdfplumber
import pandas as pd
import io

def extract_data_from_pdf(file, bbox):
    text_data = ""
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]
        cropped_page = page.crop(bbox)  # Schneide den Bereich zu
        text_data = cropped_page.extract_text(x_tolerance=3, y_tolerance=3)
    return text_data

def main():
    st.title("Bereich aus PDF extrahieren und darstellen")

    uploaded_file = st.file_uploader("Lade eine PDF-Datei hoch", type=["pdf"])
    if uploaded_file is not None:
        st.sidebar.header("Koordinaten für den PDF-Bereich")
        x0 = st.sidebar.number_input("X0 Koordinate", min_value=0, value=0)
        y0 = st.sidebar.number_input("Y0 Koordinate", min_value=0, value=0)
        x1 = st.sidebar.number_input("X1 Koordinate", min_value=0, value=100)
        y1 = st.sidebar.number_input("Y1 Koordinate", min_value=0, value=100)

        bbox = (x0, y0, x1, y1)

        if st.button("Bereich anzeigen"):
            # Zeige den ausgewählten Bereich als Vorschau
            with pdfplumber.open(uploaded_file) as pdf:
                page = pdf.pages[0]
                cropped_page = page.crop(bbox)  # Schneide den Bereich zu
                st.image(cropped_page.to_image(), caption="Ausgewählter Bereich", use_column_width=True)

        if st.button("Text extrahieren"):
            # Extrahiere Daten aus dem ausgewählten Bereich
            extracted_text = extract_data_from_pdf(uploaded_file, bbox)
            if extracted_text:
                st.text_area("Extrahierter Text", extracted_text, height=150)

                # Konvertiere den extrahierten Text in ein DataFrame
                data = [{"Extrahierter Text": line} for line in extracted_text.split('\n') if line.strip()]
                df = pd.DataFrame(data)

                # Zeige eine editierbare Tabelle an
                edited_df = st.data_editor(df)
                st.dataframe(edited_df)

main()
