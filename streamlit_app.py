import streamlit as st
import pdfplumber
from datetime import datetime, timedelta
import pytz
from icalendar import Calendar, Event

# Funktion zum Extrahieren von Text aus einem PDF
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ''.join([page.extract_text() for page in pdf.pages])
    return text

# Funktion zur Verarbeitung des Spielplans und Erstellung von Events
def process_schedule(text):
    events = []
    lines = text.split('\n')
    for line in lines:
        if 'SV Dörfleins' in line:
            # Hier die Logik zur Extraktion von Datum, Zeit und Gegner implementieren
            # Beispiel: "So. 05.05.2024 09:00 SV Dörfleins - TSV Elsa"
            parts = line.split()
            date_str = parts[1]
            time_str = parts[2]
            opponent = parts[4]  # Beispiel, abhängig vom Format

            dt_start = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")
            dt_start = pytz.timezone("Europe/Berlin").localize(dt_start)
            dt_end = dt_start + timedelta(hours=2)  # Annahme: 2 Stunden pro Spiel

            events.append({
                "dtstart": dt_start,
                "dtend": dt_end,
                "opponent": opponent
            })
    return events

# Funktion zum Erstellen eines ICS-Files
def create_ics(events):
    cal = Calendar()
    for event in events:
        cal_event = Event()
        cal_event.add('summary', f"SV Dörfleins vs {event['opponent']}")
        cal_event.add('dtstart', event['dtstart'])
        cal_event.add('dtend', event['dtend'])
        cal_event.add('location', 'SV Dörfleins')  # Ort anpassen falls erforderlich
        cal.add_component(cal_event)
    return cal.to_ical()

# Streamlit App UI
st.title("SV Dörfleins Spielplan-ICS-Generator")

uploaded_file = st.file_uploader("Laden Sie den Spielplan als PDF hoch", type=["pdf"])

if st.button('ICS-File erstellen') and uploaded_file is not None:
    # Text aus dem PDF extrahieren
    schedule_text = extract_text_from_pdf(uploaded_file)

    # Verarbeitung des Spielplans
    events = process_schedule(schedule_text)

    # Erstellung der ICS-Datei
    ics_content = create_ics(events)

    # Download-Link für die ICS-Datei
    st.download_button(
        label="Download ICS-Datei",
        data=ics_content,
        file_name="sv_doerfleins_schedule.ics",
        mime="text/calendar"
    )
