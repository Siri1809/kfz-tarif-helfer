import streamlit as st
import os
from PIL import Image

# 1. Seiteneinstellungen (Auf Smartphones optimiert)
st.set_page_config(
    page_title="Tarifrechner Helfer - Patrick Grellner Finance", 
    page_icon="🚗", 
    layout="centered"
)

# 2. BRANDING & HIGHLIGHT CSS (Interaktive Effekte wie auf Ihren Screenshots!)
st.markdown("""
    <style>
    /* Globaler, edler Hintergrund (Light Mode mit gutem Kontrast) */
    .stApp {
        background-color: #f4f6f9 !important;
        color: #2d3748 !important;
        font-family: 'Varela Round', sans-serif !important;
    }
    
    /* Hauptüberschrift in Ihrer originalen blauen Markenfarbe */
    .main-title {
        font-family: 'Varela Round', sans-serif;
        color: #0b4aa0;
        font-weight: 700;
        font-size: 2.2rem;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 5px;
    }
    
    .main-subtitle {
        text-align: center;
        color: #718096;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    
    /* Karten-Optik für die Abschnitte */
    .form-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        border: 1px solid #edf2f7;
        margin-bottom: 25px;
    }
    
    /* Bereichsüberschriften */
    .section-title {
        color: #0b4aa0;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 18px;
        border-bottom: 2px solid #00aeeb;
        padding-bottom: 8px;
    }
    
    /* KORREKTUR: Felder SCHNEEWEIẞ mit kontrastreichem grauen Rahmen */
    .stTextInput input, .stSelectbox div, .stNumberInput input, .stSelectbox [data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #0b4aa0 !important; /* Passend zum Logo */
        border: 2px solid #cbd5e0 !important; /* Deutlich sichtbarer Kontrast-Rahmen */
        border-radius: 8px !important;
        padding: 10px 14px !important;
        font-family: 'Varela Round', sans-serif !important;
        font-weight: bold !important;
        transition: all 0.25s ease-in-out !important; /* Macht den Übergang seidenweich */
    }
    
    /* INTERAKTIVER HOVER-EFFEKT (Wenn man mit der Maus darüber fährt) */
    .stTextInput input:hover, .stNumberInput input:hover, .stSelectbox div:hover {
        border-color: #00aeeb !important; /* Rahmen färbt sich in Cyan */
        background-color: #fcfdfd !important;
    }
    
    /* INTERAKTIVER FOKUS-EFFEKT (Wenn man hineinklickt - exakt wie auf Ihren Bildern!) */
    .stTextInput input:focus, .stNumberInput input:focus {
        background-color: #ffffff !important;
        border-color: #00aeeb !important;
        box-shadow: 0 0 0 4px rgba(0, 174, 235, 0.25) !important; /* Blauer Leuchteffekt */
    }

    /* Label-Texte über den Feldern (Dunkelblau passend zum Logo) */
    label {
        color: #0b4aa0 !important;
        font-weight: bold !important;
        font-size: 0.95rem !important;
        margin-bottom: 6px !important;
    }
    
    /* Premium Senden-Button */
    div.stButton > button:first-child {
        background-color: #00aeeb !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 600 !important;
        font-family: 'Varela Round', sans-serif !important;
        border-radius: 6px !important;
        padding: 14px 40px !important;
        font-size: 16px !important;
        width: 100% !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px rgba(0, 174, 235, 0.3) !important;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #0b4aa0 !important;
        box-shadow: 0 6px 20px rgba(11, 74, 160, 0.4) !important;
        transform: translateY(-1px);
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
    st.markdown("<h2 style='text-align: center; color: #0b4aa0; font-family: \"Varela Round\", sans-serif; letter-spacing: 1px;'>PATRICK GRELLNER FINANCE</h2>", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>Datenerfassung</h1>", unsafe_allow_html=True)
st.markdown("<p class='main-subtitle'>Schnell und sicher alle Daten für Ihre Autoversicherung einreichen</p>", unsafe_allow_html=True)
st.write("")

# 4. Sicherheits-Schranke: Die Kunden-PIN
KORREKTE_PIN = "1234" 

st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.markdown("<h3 style='font-size: 1.1rem; color: #0b4aa0; margin-top: 0;'>🔑 Zugang freischalten</h3>", unsafe_allow_html=True)
pin_eingabe = st.text_input("Bitte geben Sie Ihre persönliche PIN ein:", type="password", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

if pin_eingabe == KORREKTE_PIN:
    st.success("🔓 Zugang erfolgreich freigeschaltet.")
    st.write("")

    # === KARTE 1: PERSÖNLICHE DATEN ===
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown("<div class='section-title'>👤 Persönliche Daten</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Nachname *")
        vorname = st.text_input("Vorname *")
    with col2:
        geburtsort = st.text_input("Geburtsort *")
        familienstand = st.selectbox("Familienstand", ["Ledig", "Verheiratet", "Eingetragene Lebenspartnerschaft", "Geschieden", "Verwitwet"])
    st.markdown('</div>', unsafe_allow_html=True)

    # === KARTE 2: FAHRZEUG ===
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🚘 Fahrzeug & Nutzung</div>", unsafe_allow_html=True)
    
    fahrleistung = st.number_input("Jährliche Fahrleistung (in km) *", value=10000, step=1000)
    km_stand = st.number_input("Aktueller Kilometerstand (bei älteren Fahrzeugen)", value=0, step=5000)
    garage = st.selectbox("Abstellort des Fahrzeugs (Garage) *", ["Einzel-/Doppelgarage", "Tiefgarage", "Carport", "Privatgrundstück (befriedet)", "Straße / Laternenparker"])
    st.markdown('</div>', unsafe_allow_html=True)

    # === KARTE 3: DOKUMENTE ===
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📂 Dokumente hochladen</div>", unsafe_allow_html=True)
    st.info("💡 Dokumente oder Fotos können Sie ganz einfach direkt mit Ihrer Smartphone-Kamera aufnehmen.")
    
    police = st.file_uploader("Letzte Versicherungspolice *", type=["pdf", "png", "jpg", "jpeg"])
    fuehrerscheine = st.file_uploader("Führerschein Vorder- & Rückseite (aller Fahrer) *", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
    ausweise = st.file_uploader("Personalausweis Vorder- & Rückseite (aller Fahrer) *", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Pflichtfelder prüfen
    pflichtfelder_ausgefuellt = name and vorname and geburtsort and police and fuehrerscheine and ausweise

    if pflichtfelder_ausgefuellt:
        if st.button("🚀 DATEN JETZT SICHER ÜBERTRAGEN", type="primary"):
            
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
            st.success("🎉 Übertragung erfolgreich! Ihre Daten wurden sicher an uns übermittelt.")
            
            # Der fertige Kopierbereich für Sie
            st.write("---")
            st.subheader("📋 Kopierbereich für das Maklerbüro")
            st.code(infotext, language="text")

    else:
        st.warning("⚠️ Bitte füllen Sie alle mit * markierten Felder aus und laden Sie die Dokumente hoch, um die Übertragung zu starten.")

    # 6. STIMMUNGSBILD GANZ UNTEN
    st.write("") 
    THEME_BILD = "pg-finance-theme.jpg"
    if os.path.exists(THEME_BILD):
        theme_img = Image.open(THEME_BILD)
        st.image(theme_img, use_container_width=True)

else:
    if pin_eingabe != "":
        st.error("❌ Falsche PIN. Bitte prüfen Sie Ihre Eingabe.")
