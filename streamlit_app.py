import streamlit as st
import pdfplumber
import re
from datetime import datetime, timedelta
import pytz
from icalendar import Calendar, Event
from PIL import Image
import io

# Funktion zum Extrahieren von Text aus einem bestimmten Bereich des hochgeladenen PDFs
def extract_text_from_pdf_area(uploaded_file, bbox):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            cropped_page = page.crop(bbox)
            text += cropped_page.extract_text() or ""
            image_stream = io.BytesIO()
            cropped_page.to_image(resolution=150).save(image_stream, format="PNG")
            image_stream.seek(0)  # Zurücksetzen des Stream-Zeigers
            with Image.open(image_stream) as pil_image:
                st.image(pil_image)
            # Schließen und Freigeben des Bildspeichers
            image_stream.close()
    return text

# Anpassen der Logik zur korrekten Verarbeitung des Textes
def process_schedule(text, team_name, team_info):
    events = []
    lines = text.split('\n')
    date_pattern = r'(So\.|Mo\.|Di\.|Mi\.|Do\.|Fr\.|Sa\.)\d{2}\.\d{2}\.\d{4}'
    game_pattern = r'(\d{2}:\d{2})\s(.+)'
    current_date = None

    for line in lines:
        date_match = re.search(date_pattern, line)
        if date_match:
            current_date = date_match.group(0)[-10:]

        if current_date:
            game_match = re.search(game_pattern, line)
            if game_match:
                time, teams = game_match.groups()
                if team_name in teams:
                    if teams.startswith(team_name):
                        team1 = team_name
                        team2 = teams[len(team_name):].strip()
                    else:
                        team1 = teams.split(team_name)[0].strip()
                        team2 = team_name

                    datetime_str = f"{current_date} {time}"
                    dt_start = datetime.strptime(datetime_str, "%d.%m.%Y %H:%M")
                    dt_start = pytz.timezone("Europe/Berlin").localize(dt_start)
                    dt_end = dt_start + timedelta(hours=5)

                    summary = f"{team1} vs {team2}"
                    description = f"{team_info}\nMannschaft: {team_name}"
                    location = team1 if teams.index(team1) < teams.index(team2) else team2
                    events.append({"dtstart": dt_start, "dtend": dt_end, "summary": summary, "description": description, "location": location})

    return events

def create_ics(events, team_name):
    cal = Calendar()
    cal.add('prodid', f'-//{team_name}//Match Schedule//EN')
    cal.add('version', '2.0')
    utc_timezone = pytz.utc

    for event in events:
        cal_event = Event()
        cal_event.add('summary', event['summary'])
        cal_event.add('description', event['description'])
        dt_start_utc = event['dtstart'].astimezone(utc_timezone) if event['dtstart'].tzinfo else utc_timezone.localize(event['dtstart'])
        dt_end_utc = event['dtend'].astimezone(utc_timezone) if event['dtend'].tzinfo else utc_timezone.localize(event['dtend'])
        cal_event.add('dtstart', dt_start_utc)
        cal_event.add('dtend', dt_end_utc)
        cal_event.add('location', event['location'])
        cal.add_component(cal_event)

    return cal.to_ical()

# Streamlit App
st.markdown("# Spielplan-ICS-Generator :tennis:")
st.markdown("Besuchen Sie mein GitHub-Profil: [HubertWuerschinger](https://github.com/HubertWuerschinger)")
github_logo_url = "https://github.githubassets.com/assets/GitHub-Logo-ee398b662d42.png"
st.image(github_logo_url, width=100)  # Anpassen der Breite nach Bedarf

uploaded_file = st.file_uploader("Lade deinen MyBigPoint Spielplan als PDF hoch", type="pdf")

# Eingabefelder für die Koordinaten
x1 = st.number_input("X1-Koordinate", min_value=0, value=400)
y1 = st.number_input("Y1-Koordinate", min_value=0, value=100)
x2 = st.number_input("X2-Koordinate", min_value=0, value=750)
y2 = st.number_input("Y2-Koordinate", min_value=0, value=500)

if uploaded_file is not None:
    bbox = (x1, y1, x2, y2)
    schedule_text = extract_text_from_pdf_area(uploaded_file, bbox)
    schedule_text = st.text_area("Bearbeitbarer Spielplan", schedule_text, height=300)

    team_name = st.text_input("Gib den Vereinsnamen ein, genauso wie er in der Vorschau angezeigt wird", "")
    team_info = st.text_input("Gib eine Zusatzinfo für deine Mannschaft ein z.B. 1. Mannschaft Herren", "")

       if st.button('Erstelle ICS-Datei'):
        events = process_schedule(schedule_text, team_name, team_info)
        ics_content = create_ics(events, team_name)
        st.text_area("Vorschau ICS-Datei", ics_content.decode("utf-8"), height=300)
        st.download_button("Download der ICS-Datei für Outlook oder Google Kalender", data=ics_content, file_name=f"{team_name}_schedule.ics", mime="text/calendar")
    # Optional: Löschen von großen, nicht mehr benötigten Datenstrukturen
    del schedule_text, events
