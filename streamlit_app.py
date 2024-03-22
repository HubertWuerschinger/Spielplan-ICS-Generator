import streamlit as st
import pdfplumber
import pandas as pd
import re
from datetime import datetime
from PIL import Image
import io

def extract_data_from_pdf(file, bbox):
    text_data = ""
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]
        cropped_page = page.crop(bbox)
        text_data = cropped_page.extract_text(x_tolerance=3, y_tolerance=3)
    return text_data

import re
from datetime import datetime

def process_extracted_text(text):
    lines = text.split('\n')
    data = []
    last_date = None

    # Aktualisierter regulärer Ausdruck, um das komplette Datum zu erfassen
    date_pattern = re.compile(r'\w+\.\d{2}\.\d{2}\.\d{4}\d{2}:\d{2}')

    for line in lines:
        date_match = date_pattern.search(line)
        if date_match:
            # Entferne den Wochentag und konvertiere in ein datetime-Objekt
            date_str = date_match.group()
            date_str = date_str.split('.', 1)[1]  # Entferne Wochentag
            try:
                last_date = datetime.strptime(date_str, '%d.%m.%Y%H:%M')
            except ValueError as e:
                st.error(f"Fehler bei der Datumsverarbeitung: {e}")
                continue

        # Mannschaftsnamen-Logik bleibt gleich
        if " - " in line and last_date:
            teams = line.split(" - ")
            if len(teams) == 2:
                heim, gast = teams[0], teams[1]
                data.append({"Termin": last_date, "Heimmannschaft": heim.strip(), "Gastmannschaft": gast.strip()})

    return pd.DataFrame(data)



def main():
    st.title("Bereich aus PDF extrahieren und darstellen")

    uploaded_file = st.file_uploader("Lade eine PDF-Datei hoch", type=["pdf"])
    if uploaded_file is not None:
        x0 = st.sidebar.number_input("X0 Koordinate", min_value=0, value=0)
        y0 = st.sidebar.number_input("Y0 Koordinate", min_value=0, value=0)
        x1 = st.sidebar.number_input("X1 Koordinate", min_value=0, value=100)
        y1 = st.sidebar.number_input("Y1 Koordinate", min_value=0, value=100)

        bbox = (x0, y0, x1, y1)

        if st.button("Bereich anzeigen"):
            with pdfplumber.open(uploaded_file) as pdf:
                page = pdf.pages[0]
                cropped_page = page.crop(bbox)
                # Konvertiere PageImage in PIL.Image
                image_stream = io.BytesIO()
                cropped_page.to_image().save(image_stream, format="PNG")
                cropped_image = Image.open(image_stream)
                st.image(cropped_image, caption="Ausgewählter Bereich", use_column_width=True)

        if st.button("Text extrahieren"):
            extracted_text = extract_data_from_pdf(uploaded_file, bbox)
            if extracted_text:
                st.text_area("Extrahierter Text", extracted_text, height=150)
                df = process_extracted_text(extracted_text)
                if not df.empty:
                    edited_df = st.data_editor(df)
                    st.dataframe(edited_df)
                else:
                    st.error("Keine Daten in der Tabelle gefunden. Bitte überprüfe den extrahierten Text und die Verarbeitungslogik.")

main()
