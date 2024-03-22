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
        parts = line.split()
        if not parts:
            continue

        # Erkenne und speichere das Datum, wenn vorhanden
        if re.match(r'\d{2}\.\d{2}\.\d{4}', parts[0]):
            last_date = datetime.strptime(parts.pop(0), '%d.%m.%Y').date()

        # Gehe zur nächsten Zeile, falls keine Uhrzeit gefunden wird
        if not re.match(r'\d{2}:\d{2}', parts[0]):
            continue

        # Entferne die Uhrzeit und behalte den Rest
        parts.pop(0)  # Entferne Uhrzeit
        team_line = ' '.join(parts)

        # Trenne Heim- und Gastmannschaft
        if " - " in team_line:
            heim, gast = team_line.split(" - ", 1)
            data.append({"Datum": last_date, "Heim": heim.strip(), "Gast": gast.strip()})

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
