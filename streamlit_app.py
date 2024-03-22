import streamlit as st
import pdfplumber
import pandas as pd
import re
from datetime import datetime
from PIL import Image
import io

def extract_data_from_pdf(file, bbox):
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]
        cropped_page = page.crop(bbox)
        text = cropped_page.extract_text(x_tolerance=3, y_tolerance=3)
    return text

def process_extracted_text(text):
    lines = text.split('\n')
    data = []
    last_date = None

    for line in lines:
        # Ignoriere den Wochentag und extrahiere das Datum
        date_match = re.search(r'\d{2}\.\d{2}\.\d{4}', line)
        if date_match:
            date_str = date_match.group()
            last_date = datetime.strptime(date_str, '%d.%m.%Y').date()

        # Extrahiere die Uhrzeit
        time_match = re.search(r'\d{2}:\d{2}', line)
        if time_match:
            time_str = time_match.group()
            # Entferne Datum, Uhrzeit und etwaige Wochentage, um die Mannschaften zu isolieren
            team_line = re.sub(r'\w+\.\d{2}\.\d{2}\.\d{4}\d{2}:\d{2}', '', line).strip()
            teams = team_line.split(maxsplit=2)  # Trenne in Heim- und Gastmannschaft

            if len(teams) >= 2 and last_date:
                heim, gast = teams[0], teams[1]
                data.append({"Datum": last_date, "Uhrzeit": time_str, "Heim": heim, "Gast": gast})

    return pd.DataFrame(data)





def main():
    st.title("Bereich aus PDF extrahieren und darstellen")

    uploaded_file = st.file_uploader("Lade eine PDF-Datei hoch", type=["pdf"])

    # Zustandsvariable für den extrahierten Text
    if 'extracted_text' not in st.session_state:
        st.session_state['extracted_text'] = ''

    if uploaded_file is not None:
        x0 = st.sidebar.number_input("X0 Koordinate", min_value=0, value=0)
        y0 = st.sidebar.number_input("Y0 Koordinate", min_value=0, value=0)
        x1 = st.sidebar.number_input("X1 Koordinate", min_value=0, value=100)
        y1 = st.sidebar.number_input("Y1 Koordinate", min_value=0, value=100)

        bbox = (x0, y0, x1, y1)

        if st.button("Bereich anzeigen"):
            st.session_state['extracted_text'] = extract_data_from_pdf(uploaded_file, bbox)
            with pdfplumber.open(uploaded_file) as pdf:
                page = pdf.pages[0]
                cropped_page = page.crop(bbox)
                image_stream = io.BytesIO()
                cropped_page.to_image().save(image_stream, format="PNG")
                cropped_image = Image.open(image_stream)
                st.image(cropped_image, caption="Ausgewählter Bereich", use_column_width=True)

        text_area = st.text_area("Extrahierter Text", st.session_state['extracted_text'], height=150)

        if st.button("Tabelle aktualisieren"):
            if text_area:
                df = process_extracted_text(text_area)
                st.data_editor(df)
            else:
                st.error("Bitte gib zuerst Text in das Textfeld ein oder zeige einen Bereich an.")

main()
