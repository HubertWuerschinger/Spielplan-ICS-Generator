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



# Funktion zum Erstellen eines ICS- oder iCal-Files
def create_calendar_file(events, file_format="ics"):
    cal = Calendar()
    cal.add('prodid', '-//MeineFirma//MeinKalenderProdukt//DE')
    cal.add('version', '2.0')

    for event in events:
        cal_event = Event()
        cal_event.add('summary', f"SV Dörfleins vs {event['opponent']}")
        cal_event.add('dtstart', event['dtstart'])
        cal_event.add('dtend', event['dtend'])
        cal_event.add('location', 'SV Dörfleins' if event['home'] else 'Away')
        cal.add_component(cal_event)
        st.text(f"Adding event: {event}")  # Zeigt die hinzugefügten Events an

    return cal.to_ical()


# Streamlit App UI
st.title("SV Dörfleins Spielplan-ICS/iCal-Generator")

# Upload-Feld für das PDF
uploaded_file = st.file_uploader("Laden Sie den Spielplan als PDF hoch", type="pdf")

if uploaded_file is not None and st.button('Dateien erstellen'):
    # Text aus dem PDF extrahieren
    schedule_text = extract_text_from_pdf(uploaded_file)

    # Verarbeitung des Spielplans
    events = process_schedule(schedule_text)

    # Erstellung der ICS- und iCal-Dateien
    calendar_content = create_calendar_file(events)

    # Erstellung der Download-Links
    st.download_button(
        label="Download ICS-Datei",
        data=calendar_content,
        file_name="sv_doerfleins_schedule.ics",
        mime="text/calendar"
    )
    
    st.download_button(
        label="Download iCal-Datei",
        data=calendar_content,
        file_name="sv_doerfleins_schedule.ical",
        mime="text/calendar"
    )
