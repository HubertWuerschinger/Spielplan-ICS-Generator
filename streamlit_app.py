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
            # Konvertieren in ein PIL-Image und Anzeigen der Vorschau
            image_stream = io.BytesIO()
            cropped_page.to_image(resolution=150).save(image_stream, format="PNG")
            pil_image = Image.open(image_stream)
            st.image(pil_image)
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
                    # Teilt den String basierend auf der Position von "SV Dörfleins"
                    if teams.startswith(team_name):
                        team1 = team_name
                        team2 = teams[len(team_name):].strip()
                    else:
                        team1 = teams.split(team_name)[0].strip()
                        team2 = team_name

                    datetime_str = f"{current_date} {time}"
                    dt_start = datetime.strptime(datetime_str, "%d.%m.%Y %H:%M")
                    dt_start = pytz.timezone("Europe/Berlin").localize(dt_start)
                    
                    # Endzeit auf 5 Stunden nach dem Startzeitpunkt festlegen
                    dt_end = dt_start + timedelta(hours=5)

                    summary = f"{team1} vs {team2}"
                    description = f"{team_info}\nMannschaft: {team_name}"
                    location = team_name  # Ort des Vereins als Ort im Kalender verwenden
                    events.append({"dtstart": dt_start, "dtend": dt_end, "summary": summary, "description": description, "location": location})

    return events


# Funktion zur Erstellung des ICS-Dateiinhalts
def create_ics(events, team_name):
    cal = Calendar()
    cal.add('prodid', f'-//{team_name}//Match Schedule//EN')  # Verwenden Sie team_name im PRODID
    cal.add('version', '2.0')
    for event in events:
        cal_event = Event()
        cal_event.add('summary', event['summary'])
        cal_event.add('description', event['description'])
        cal_event.add('dtstart', event['dtstart'])
        cal_event.add('dtend', event['dtend'])
        cal_event.add('location', event['location'])  # Ort hinzufügen
        cal.add_component(cal_event)
    return cal.to_ical()

# Streamlit App
st.markdown("# Spielplan-ICS-Generator :tennis:")

# Verwenden von st.markdown, um den Link zu Ihrem GitHub-Profil anzuzeigen
st.markdown("Besuchen Sie mein GitHub-Profil: [HubertWuerschinger](https://github.com/HubertWuerschinger)")

# Anzeige des GitHub-Logos mit st.image
github_logo_url = "https://github.githubassets.com/assets/GitHub-Logo-ee398b662d42.png"
st.image(github_logo_url, width=100)  # Anpassen der Breite nach Bedarf

uploaded_file = st.file_uploader("Lade deinen MyBigPoint Spielplan als PDF hoch", type="pdf")

# Eingabefelder für die Koordinaten
st.write=("Passe die Koordinaten für den relevanten Bereich an, falls notwendig")
x1 = st.number_input("X1-Koordinate", min_value=0, value=400)
y1 = st.number_input("Y1-Koordinate", min_value=0, value=100)
x2 = st.number_input("X2-Koordinate", min_value=0, value=750)
y2 = st.number_input("Y2-Koordinate", min_value=0, value=500)

if uploaded_file is not None:
    bbox = (x1, y1, x2, y2)
    schedule_text = extract_text_from_pdf_area(uploaded_file, bbox)
    schedule_text = st.text_area
