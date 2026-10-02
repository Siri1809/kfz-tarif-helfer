import streamlit as st
import os
from PIL import Image

# 1. Seiteneinstellungen (Optimiert für Smartphones)
st.set_page_config(
    page_title="Kfz-Tarifrechner Helfer", 
    page_icon="🚗", 
    layout="centered"
)

# 2. Logo einbinden (Falls vorhanden)
LOGO_DATEINAME = "image.png"
if os.path.exists(LOGO_DATEINAME):
    logo = Image.open(LOGO_DATEINAME)
    # Zeigt das Logo zentriert und in einer angenehmen Breite an
    st.image(logo, width=250)
else:
    st.subheader("Büro für Versicherungen") # Fallback, falls das Logo mal fehlt

st.title("🚗 Datenerfassung für Autoversicherung")
st.write("Tragen Sie hier bequem Ihre Daten ein. Wir berechnen das beste Angebot für Sie.")

# 3. Sicherheits-Schranke: Die Kunden-PIN
# Sie können die PIN hier im Code ändern (z.B. "BOSCH2026")
KORREKTE_PIN = "1234" 

pin_eingabe = st.text_input("🔑 Bitte geben Sie Ihre persönliche Kunden-PIN ein:", type="password")

if pin_eingabe == KORREKTE_PIN:
    st.success("Freigeschaltet! Sie können jetzt Ihre Daten eingeben.")
    st.write("---")

    # 4. Eingabemaske für den Kunden
    st.subheader("📋 Persönliche Daten")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name *")
        vorname = st.text_input("Vorname *")
    with col2:
        geburtsort = st.text_input("Geburtsort *")
        familienstand = st.selectbox("Familienstand", ["Ledig", "Verheiratet", "Eingetragene Lebenspartnerschaft", "Geschieden", "Verwitwet"])

    st.subheader("🚘 Fahrzeug & Nutzung")
    fahrleistung = st.number_input("Jährliche Fahrleistung (in km) *", value=10000, step=1000)
    km_stand = st.number_input("Aktueller Kilometerstand (bei älteren Fahrzeugen)", value=0, step=5000)
    garage = st.selectbox("Abstellort des Fahrzeugs (Garage)", ["Einzel-/Doppelgarage", "Tiefgarage", "Carport", "Privatgrundstück (befriedet)", "Straße / Laternenparker"])

    st.subheader("📂 Dokumente hochladen")
    st.info("💡 Tipp: Sie können Dokumente direkt mit der Smartphone-Kamera fotografieren.")
    
    police = st.file_uploader("Letzte Versicherungspolice (PDF oder Foto) *", type=["pdf", "png", "jpg", "jpeg"])
    fuehrerscheine = st.file_uploader("Führerschein Vorder- und Rückseite (aller Fahrer) *", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
    ausweise = st.file_uploader("Personalausweis Vorder- und Rückseite (aller Fahrer) *", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)

    st.write("---")

    # Aktivierungs-Logik für den Senden-Button (Pflichtfelder prüfen)
    pflichtfelder_ausgefuellt = name and vorname and geburtsort and police and fuehrerscheine and ausweise

    if pflichtfelder_ausgefuellt:
        if st.button("🚀 Daten & Dokumente sicher übertragen", type="primary"):
            
            # Ordnerstruktur für Sie erstellen
            ordner_name = f"Kunde_{name}_{vorname}"
            if not os.path.exists(ordner_name):
                os.makedirs(ordner_name)
            
            # Dateien lokal auf dem Server speichern (für den Testlauf)
            if police:
                with open(os.path.join(ordner_name, f"Police_{police.name}"), "wb") as f:
                    f.write(police.getbuffer())
            
            for i, fs in enumerate(fuehrerscheine):
                with open(os.path.join(ordner_name, f"FS_{i}_{fs.name}"), "wb") as f:
                    f.write(fs.getbuffer())

            for i, aus in enumerate(ausweise):
                with open(os.path.join(ordner_name, f"Ausweis_{i}_{aus.name}"), "wb") as f:
                    f.write(aus.getbuffer())

            # Formatierte Textdatei für Ihr Copy-Paste erzeugen
            infotext = f"""=== KUNDENDATEN FÜR NAFI / COMPARIT ===
Name: {name}
Vorname: {vorname}
Geburtsort: {geburtsort}
Familienstand: {familienstand}
----------------------------------------
Fahrleistung: {fahrleistung} km/Jahr
Aktueller KM-Stand: {km_stand} km
Garage: {garage}
========================================"""

            with open(os.path.join(ordner_name, "Kopier_Vorlage.txt"), "w", encoding="utf-8") as f:
                f.write(infotext)

            st.balloons() # Schöner visueller Effekt bei Erfolg!
            st.success("🎉 Übertragung erfolgreich! Vielen Dank für Ihre Mühe. Sie können das Browserfenster jetzt schließen.")
            
            # Der fertige Kopierbereich wird nach dem Absenden für Sie eingeblendet
            st.write("---")
            st.subheader("📋 Kopierbereich für das Maklerbüro")
            st.info("Klicken Sie oben rechts im grauen Feld auf das Kopiersymbol, um alle Daten für NAFI/Comparit zu kopieren.")
            st.code(infotext, language="text")

    else:
        st.warning("⚠️ Bitte füllen Sie alle mit * markierten Felder aus und laden Sie die erforderlichen Dokumente hoch, um das Formular absenden zu können.")

else:
    if pin_eingabe != "":
        st.error("❌ Falsche PIN. Bitte prüfen Sie Ihre Eingabe.")
