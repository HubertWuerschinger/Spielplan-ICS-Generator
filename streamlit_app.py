import streamlit as st
import pdfplumber
from datetime import datetime, timedelta
import pytz
from icalendar import Calendar, Event
import re

# Funktion zum Extrahieren von Text aus einem PDF
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ''.join([page.extract_text() for page in pdf.pages])
    return text

# Funktion zur Verarbeitung des Spielplans und Erstellung von Events


def process_schedule(text):
    events = []
    lines = text.split('\n')

    # Regex-Muster zur Identifizierung von Spielzeilen
    match_pattern = r'(So\.|Do\.)\d{2}\.\d{2}\.\d{4}\d{2}:\d{2} .+ .+'

    for line in lines:
        # Überprüfe, ob die Zeile einem Spiel entspricht
        if re.match(match_pattern, line):
            try:
                # Extrahiere Datum, Uhrzeit und Teams
                parts = re.split(r'(\d{2}\.\d{2}\.\d{4})(\d{2}:\d{2})', line)
                date_str, time_str, teams = parts[1], parts[2], parts[3].strip()

                dt_start = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")
                dt_start = pytz.timezone("Europe/Berlin").localize(dt_start)
                dt_end = dt_start + timedelta(hours=2)

                home_team, away_team = teams.split('-')
                home_game = "SV Dörfleins" in home_team

                opponent = away_team if home_game else home_team
                events.append({
                    "dtstart": dt_start,
                    "dtend": dt_end,
                    "opponent": opponent.strip(),
                    "home": home_game
                })
            except Exception as e:
                st.error(f"Fehler beim Parsen der Zeile: {line} - {e}")
                continue
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
