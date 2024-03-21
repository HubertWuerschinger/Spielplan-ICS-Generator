import streamlit as st
import pandas as pd
from pandas.core.tools.datetimes import to_datetime

def convert_to_datetime(df, date_column):
    df[date_column] = pd.to_datetime(df[date_column])
    return df

# Streamlit App Start
st.title("Termine aus PDF extrahieren")

# Beispiel eines DataFrames
dates_data = [
    {"Datum": "2024-01-01", "Ereignis": "Neujahr"},
    {"Datum": "2024-03-20", "Ereignis": "Frühlingsanfang"}
]
df = pd.DataFrame(dates_data)

# Konvertiere das Datum in datetime
df = convert_to_datetime(df, "Datum")

# Zeige eine editierbare Tabelle an
edited_df = st.data_editor(df)

if not edited_df.empty:
    # Stelle sicher, dass das Datum als datetime formatiert ist
    edited_df = convert_to_datetime(edited_df, "Datum")
    
    # Finde das Ereignis mit dem neuesten Datum
    favorite_event = edited_df.loc[edited_df["Datum"].idxmax()]["Ereignis"]
    st.markdown(f"Dein ausgewähltes Ereignis ist **{favorite_event}** 🎈")

# Streamlit App Ende
