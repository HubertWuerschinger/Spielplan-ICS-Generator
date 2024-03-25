# Spielplan-ICS-Generator :tennis:
Erstellung von ICS Files für die Mannschaftspiele aus MyBigPoint PDF
Stürzt bei der Erstellung der ICS Files manchmal ab, dann die Streamlit App rebooten rechts im Menü
Stand 25.03.2024
 \
 \
**Herausforderungen bei der Erstellung:**
  1. Extraktion der Spieltabelle. Zuschneiden des PDF Dokumentes auf die Tabelle, diese befindet sich von den Koordinaten immer an der gleichen Stelle
  2. Parsing der Tabelleninformationen. Der Spieltag an dem mehrere Spiele sind beginnt mit der Abkürzung für den Wochentag,
     gefolgt vom Datum und Uhrzeit mit Leerzeichen, Punkt und ohne Leerzeichen. Danach in weiteren Spalten ist nur die Uhrzeit bezogen auf das vorherige Datum des Spieltages. Die Mannschaften Gast und Heim sind zwar durch Leerzeichen getrennt, aber es stehen vor dem Vereinsnamen Abkürzungen für TC,
     SV etc.
  3. Format des ICS Files für die Spiele. Zeitzone muss richtig gesetzt werden (UTC), da in der Vorschau die Zeit richtig angezeigt wird, aber beim Import in Outlook oder Google dann um eine Stunde in der Zukunft liegt.
  4. Abstürzten der Streamlit App bei Erstellung des ICS Files. Hier wurde noch keine Lösung gefunden. Reboot der App notwendig.

Für die Programmierung wurde ChatGPT genutzt
 \
 \
English Version translated with DeepL:
# Match schedule ICS generator :tennis:
Creation of ICS files for the team matches from MyBigPoint PDF
Sometimes crashes when creating ICS files, then reboot the Streamlit app on the right in the menu
Status 25.03.2024


**Challenges during creation:**
  1. extraction of the game table. Cropping the PDF document to the table, which is always in the same place in terms of coordinates
  2. parsing the table information. The match day on which there are several matches begins with the abbreviation for the day of the week,
     followed by the date and time with spaces, full stops and no spaces. Then in further columns only the time is related to the previous date of the match day. The teams guest and home are separated by spaces, but there are abbreviations for TC,
     SV etc.
  3. format of the ICS file for the matches. Time zone must be set correctly (UTC), as the time is displayed correctly in the preview, but is then one hour in the future when imported into Outlook or Google.
  4. crashing of the Streamlit app when creating the ICS file. No solution has been found yet. Reboot of the app necessary.
\
ChatGPT was used for the programming
\
Translated with DeepL.com (free version)
