import streamlit as st
import os
from PIL import Image

# 1. Seiteneinstellungen (Auf Smartphones optimiert)
st.set_page_config(
    page_title="Tarifrechner Helfer - Patrick Grellner Finance", 
    page_icon="🚗", 
    layout="centered"
)

# 2. BRANDING CSS (Farben & Hintergrundbild exakt von pg-finance.de kopiert)
st.markdown("""
    <style>
    /* Hintergrundbild der originalen Mobil-Landingpage einbinden */
    .stApp {
        background-image: linear-gradient(rgba(13, 27, 42, 0.85), rgba(13, 27, 42, 0.95)), 
                          url("https://pg-finance.de/wp-content/uploads/2024/02/Background_Landing_Page_Mobil_2-1024x639.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #ffffff !important;
        font-family: 'Varela Round', 'Varela', sans-serif !important;
    }
    
    /* Eingabefelder an das dunkle Design anpassen */
    .stTextInput input, .stSelectbox div, .stNumberInput input {
        background-color: rgba(27, 38, 59, 0.9) !important;
        color: #ffffff !important;
        border: 1px solid #415a77 !important;
        border-radius: 6px !important;
        font-family: 'Varela Round', sans-serif !important;
    }
    
    /* Fokus auf Eingabefelder leuchtet im originalen Cyan-Blau (#00aeeb) */
    .stTextInput input:focus {
        border-color: #00aeeb !important;
        box-shadow: 0 0 10px #00aeeb !important;
    }

    /* Überschriften in der originalen Akzentfarbe (#00aeeb) */
    h1, h2, h3, .stSubheader {
        color: #00aeeb !important;
        font-family: 'Varela Round', sans-serif !important;
        font-weight: bold;
    }
    
    /* Den Senden-Button exakt wie auf der Website stylen */
    div.stButton > button:first-child {
        background-color: #00aeeb !important;
        color: #ffffff !important;
        border: 1px solid #ffffff !important;
        font-weight: bold !important;
        font-family: 'Varela Round', sans-serif !important;
        border-radius: 4px !important;
        padding: 12px 30px !important;
        font-size: 16px !important;
        transition: all 0.3s ease;
        box-shadow: 0px 4px 15px rgba(0, 174, 235, 0.3);
    }
    
    /* Hover-Effekt des Buttons mit dem originalen Dunkelblau (#0b4aa0) */
    div.stButton > button:first-child:hover {
        background-color: #0b4aa0 !important;
        border-color: #ffffff !important;
        box-shadow: 0px 6px 20px rgba(11, 74, 160, 0.6) !important;
        transform: translateY(-2px);
    }

    /* Infoboxen (Tipps) dezent dunkelblau stylen */
    .stAlert {
        background-color: rgba(11, 74, 160, 0.2) !important;
        border: 1px solid #00aeeb !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Logo einbinden & zentrieren
LOGO_DATEINAME = "pg-finance_Logo.jpg"
if os.path.exists(LOGO_DATEINAME):
    logo = Image.open(LOGO_DATEINAME)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(logo, use_container_width=True)
else:
    st.markdown("<h2 style='text-align: center; color: #00aeeb; font-family: \"Varela Round\", sans-serif;'>PATRICK GRELLNER FINANCE</h2>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🚗 Datenerfassung für Autoversicherung</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #e0e0e0; font-size: 1.1rem;'>Tragen Sie hier bequem Ihre Daten ein. Wir berechnen das beste Angebot für Sie.</p>", unsafe_allow_html=True)
st.write("---")

# 4. Sicherheits-Schranke: Die Kunden-PIN
KORREKTE_PIN = "1234" 

st.markdown("<h3 style='font-size: 1.1rem; color: #00aeeb;'>🔑 Zugangssperre</h3>", unsafe_allow_html=True)
pin_eingabe = st.text_input("Bitte geben Sie Ihre persönliche Kunden-PIN ein, um das Formular freizuschalten:", type="password", label_visibility="collapsed")

if pin_eingabe == KORREKTE_PIN:
    st.success("🔓 Freigeschaltet! Sie können jetzt Ihre Daten eingeben.")
    st.write("---")

    # 5. Eingabemaske für den Kunden
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

    # Pflichtfelder prüfen
    pflichtfelder_ausgefuellt = name and vorname and geburtsort and police and fuehrerscheine and ausweise

    if pflichtfelder_ausgefuellt:
        if st.button("🚀 Daten & Dokumente sicher übertragen", type="primary"):
            
            # Ordnerstruktur erstellen
            ordner_name = f"Kunde_{name}_{vorname}"
            if not os.path.exists(ordner_name):
                os.makedirs(ordner_name)
            
            # Dateien speichern
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

            st.balloons()
            st.success("🎉 Übertragung erfolgreich! Vielen Dank für Ihre Mühe. Sie können das Browserfenster jetzt schließen.")
            
            # Der fertige Kopierbereich für Sie
            st.write("---")
            st.subheader("📋 Kopierbereich für das Maklerbüro")
            st.code(infotext, language="text")

    else:
        st.warning("⚠️ Bitte füllen Sie alle mit * markierten Felder aus und laden Sie die erforderlichen Dokumente hoch, um das Formular absenden zu können.")

    # 6. STIMMUNGSBILD GANZ UNTEN (Für den Kunden sichtbar, solange er ausfüllt)
    st.write("") # Abstandhalter
    THEME_BILD = "pg-finance-theme.jpg"
    if os.path.exists(THEME_BILD):
        theme_img = Image.open(THEME_BILD)
        # Zeigt das Auto-Bild zentriert ganz unten an
        st.image(theme_img, use_container_width=True, caption="Ihr Partner für sichere Wege.")

else:
    if pin_eingabe != "":
        st.error("❌ Falsche PIN. Bitte prüfen Sie Ihre Eingabe.")
