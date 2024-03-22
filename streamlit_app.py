import streamlit as st
from datetime import datetime, timedelta
import pytz
from icalendar import Calendar, Event

# Funktion zum Erstellen eines ICS-Files aus den Spielplandaten
def create_ics(events):
    cal = Calendar()
    for event in events:
        cal_event = Event()
        cal_event.add('summary', f"SV Dörfleins vs {event['opponent']}")
        cal_event.add('dtstart', event['dtstart'])
        cal_event.add('dtend', event['dtend'])
        cal_event.add('location', 'SV Dörfleins' if event['home'] else 'Away')
        cal.add_component(cal_event)
    return cal.to_ical()

# Funktion zur Verarbeitung des eingegebenen Spielplans
def process_schedule(schedule):
    events = []
    for line in schedule.split('\n'):
        try:
            date_str, time, opponents = line.split(',')
            date = datetime.strptime(date_str, "%d.%m.%Y")
            time = datetime.strptime(time, "%H:%M").time()
            dtstart = pytz.timezone("Europe/Berlin").localize(datetime.combine(date, time))
            dtend = dtstart + timedelta(hours=2)  # Annahme: 2 Stunden pro Spiel
            home, opponent = opponents.split('-')
            events.append({
                "dtstart": dtstart,
                "dtend": dtend,
                "opponent": opponent.strip(),
                "home": home.strip() == "SV Dörfleins"
            })
        except ValueError:
            st.error("Fehler beim Parsen der Zeile: " + line)
    return events

# Streamlit App UI
st.title("SV Dörfleins Spielplan-ICS-Generator")

# Eingabefeld für den Spielplan
schedule_input = st.text_area("Geben Sie den Spielplan ein (Datum, Zeit, Teams):", height=150)

if st.button('ICS-File erstellen'):
    # Verarbeitung der Eingabe
    events = process_schedule(schedule_input)

    # Erstellung der ICS-Datei
    ics_content = create_ics(events)

    # Erstellung des Download-Links
    st.download_button(
        label="Download ICS-Datei",
        data=ics_content,
        file_name="sv_doerfleins_schedule.ics",
        mime="text/calendar"
    )
