import streamlit as st
import pdfplumber
import re
from datetime import datetime, timedelta
import pytz
from icalendar import Calendar, Event

# Funktion zum Extrahieren von Text aus einem hochgeladenen PDF
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ''.join([page.extract_text() for page in pdf.pages])
    return text

# Funktion zur Verarbeitung des Spielplans und Erstellung von Events
def process_schedule(text):
    events = []
    lines = text.split('\n')
    date_pattern = r'(\d{2}\.\d{2}\.\d{4})'
    game_pattern = r'(\d{2}:\d{2})\s(.+?)-(.+)'
    current_date = None

    for line in lines:
        date_match = re.search(date_pattern, line)
        if date_match:
            current_date = date_match.group(1)

        if current_date:
            game_match = re.search(game_pattern, line)
            if game_match:
                time, team1, team2 = game_match.groups()
                datetime_str = f"{current_date} {time}"
                dt_start = datetime.strptime(datetime_str, "%d.%m.%Y %H:%M")
                dt_start = pytz.timezone("Europe/Berlin").localize(dt_start)
                dt_end = dt_start + timedelta(hours=2)
                summary = f"{team1.strip()} vs {team2.strip()}"
                events.append({"dtstart": dt_start, "dtend": dt_end, "summary": summary})

    return events

# Funktion zur Erstellung des ICS-Dateiinhalts
def create_ics(events):
    cal = Calendar()
    cal.add('prodid', '-//SV Doerfleins//Match Schedule//EN')
    cal.add('version', '2.0')
    for event in events:
        cal_event = Event()
        cal_event.add('summary', event['summary'])
        cal_event.add('dtstart', event['dtstart'])
        cal_event.add('dtend', event['dtend'])
        cal.add_component(cal_event)
    return cal.to_ical()

# Streamlit App
st.title("SV Dörfleins Spielplan-ICS-Generator")

uploaded_file = st.file_uploader("Laden Sie den Spielplan als PDF hoch", type="pdf")

if uploaded_file is not None:
    schedule_text = extract_text_from_pdf(uploaded_file)
    schedule_text = st.text_area("Bearbeitbarer Spielplan", schedule_text, height=300)
    processed_events = process_schedule(schedule_text)
    ics_content = create_ics(processed_events)
    st.download_button("Download ICS-Datei", data=ics_content, file_name="sv_doerfleins_schedule.ics", mime="text/calendar")
