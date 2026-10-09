import streamlit as st
import os
from PIL import Image

# 1. Seiteneinstellungen (Auf Smartphones optimiert)
st.set_page_config(
    page_title="Tarifrechner Helfer - Patrick Grellner Finance", 
    page_icon="🚗", 
    layout="centered"
)

# 2. BRANDING, SEAMLESS CARD & SPACING CSS
st.markdown("""
    <style>
    /* Hintergrund zu 100% reinweiß */
    .stApp {
        background-color: #ffffff !important;
        background-image: none !important;
        color: #2d3748 !important;
        font-family: 'Varela Round', 'Varela', sans-serif !important;
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
        margin-bottom: 20px;
    }
    
    /* Karten-Optik für die Abschnitte (Mit extrem sauberer Ausrichtung) */
    .form-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #edf2f7;
        margin-top: 0px !important;
        margin-bottom: 25px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
    }
    
    /* KORREKTUR: Erzwingt, dass die HTML-Überschriften in den Karten perfekt aussehen */
    .card-header {
        color: #0b4aa0 !important;
        font-size: 1.35rem !important;
        font-weight: bold !important;
        font-family: 'Varela Round', sans-serif !important;
        margin-top: 0px !important;
        margin-bottom: 20px !important;
        border-bottom: 2px solid #00aeeb !important;
        padding-bottom: 8px !important;
        display: block !important;
    }
    
    /* Ränder der Eingabefelder im originalen edlen Cyan-Blau (#00aeeb) */
    .stTextInput input, .stNumberInput input {
        background-color: #ffffff !important;
        color: #0b4aa0 !important;
        border: 2px solid #00aeeb !important;
        border-radius: 6px !important;
        padding: 10px 14px !important;
        font-family: 'Varela Round', sans-serif !important;
        font-weight: bold !important;
        outline: none !important;
        box-shadow: none !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    .stTextInput div[data-baseweb="input"], .stNumberInput div[data-baseweb="input"] {
        border: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }
    
    /* Seamless Optik für Selectboxen */
    .stSelectbox div[role="button"], 
    .stSelectbox div[data-baseweb="select"], 
    .stSelectbox [data-baseweb="select"] > div {
        border: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background-color: #ffffff !important;
        border: 2px solid #00aeeb !important;
        border-radius: 6px !important;
        font-family: 'Varela Round', sans-serif !important;
        font-weight: bold !important;
        box-shadow: none !important;
        outline: none !important;
        padding: 2px 4px !important;
    }
    
    /* Textfarbe in Auswahllisten erzwingen */
    .stSelectbox span, .stSelectbox div {
        color: #0b4aa0 !important;
        font-weight: bold !important;
    }
    
    /* HOVER- & FOKUS-EFFEKTE */
    .stTextInput input:hover, .stNumberInput input:hover, .stSelectbox [data-baseweb="select"]:hover {
        border-color: #0b4aa0 !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox [data-baseweb="select"]:focus {
        border-color: #0b4aa0 !important;
        box-shadow: 0 0 0 3px rgba(11, 74, 160, 0.2) !important;
    }

    /* Gestaltete Uploader-Boxen passend zum Design */
    [data-testid="stFileUploaderDropzone"] {
        border: 2px dashed #00aeeb !important;
        background-color: #f7fafc !important;
        border-radius: 8px !important;
        padding: 15px !important;
        box-shadow: none !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: #0b4aa0 !important;
        background-color: #edf2f7 !important;
    }
    
    [data-testid="stFileUploaderDropzone"] span {
        color: #718096 !important;
        font-size: 12px !important;
    }
    
    /* "Browse Files" Button */
    .stFileUploader button {
        background-color: #00aeeb !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: bold !important;
        font-family: 'Varela Round', sans-serif !important;
        font-size: 13px !important;
        padding: 6px 14px !important;
        border-radius: 6px !important;
        box-shadow: 0 2px 6px rgba(0, 174, 235, 0.2) !important;
    }

    /* Info-Boxen Text */
    .stAlert p, .stAlert span, .stAlert div {
        color: #1a1a1a !important;
        font-weight: bold !important;
    }

    /* Label-Texte über den Feldern */
    label {
        color: #0b4aa0 !important;
        font-weight: bold !important;
        font-size: 0.95rem !important;
        margin-bottom: 6px !important;
    }
    
    /* Senden-Button */
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
        box-shadow: 0 4px 14px rgba(0, 174, 235, 0.2) !important;
        margin-bottom: 20px !important;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #0b4aa0 !important;
        box-shadow: 0 6px 20px rgba(11, 74, 160, 0.3) !important;
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

# 4. Sicherheits-Schranke: Die Kunden-PIN
KORREKTE_PIN = "1234" 

st.markdown("""
    <div class="form-card">
        <span class="card-header">Zugang freischalten</span>
""", unsafe_allow_html=True)
pin_eingabe = st.text_input("PIN-Eingabe", type="password", label_visibility="collapsed", placeholder="Bitte PIN eingeben...")
st.markdown('</div>', unsafe_allow_html=True)

if pin_eingabe == KORREKTE_PIN:
    st.success("🔓 Zugang erfolgreich freigeschaltet.")

    # === KARTE 1: PERSÖNLICHE DATEN (Überschrift als HTML direkt in der Karte!) ===
    st.markdown("""
        <div class="form-card">
            <span class="card-header">Persönliche Daten</span>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Nachname *")
        vorname = st.text_input("Vorname *")
    with col2:
        geburtsort = st.text_input("Geburtsort *")
        familienstand = st.selectbox("Familienstand", ["Ledig", "Verheiratet", "Eingetragene Lebenspartnerschaft", "Geschieden", "Verwitwet"])
    st.markdown('</div>', unsafe_allow_html=True)

    # === KARTE 2: FAHRZEUG (Überschrift als HTML direkt in der Karte!) ===
    st.markdown("""
        <div class="form-card">
            <span class="card-header">Fahrzeug & Nutzung</span>
    """, unsafe_allow_html=True)
    
    col_fz1, col_col2 = st.columns(2)
    with col_fz1:
        fahrleistung = st.number_input("Jährliche Fahrleistung (in km) *", value=10000, step=1000)
        km_stand = st.number_input("Aktueller Kilometerstand", value=0, step=5000)
    with col_col2:
        garage = st.selectbox("Abstellort des Fahrzeugs (Garage) *", ["Einzel-/Doppelgarage", "Tiefgarage", "Carport", "Privatgrundstück (befriedet)", "Straße / Laternenparker"])
    
    st.write("") # Abstandhalter
    fahrzeugschein = st.file_uploader("Fahrzeugschein hier hochladen/fotografieren *", type=["pdf", "png", "jpg", "jpeg"])
    st.markdown('</div>', unsafe_allow_html=True)

    # === KARTE 3: DOKUMENTE (Überschrift als HTML direkt in der Karte!) ===
    st.markdown("""
        <div class="form-card">
            <span class="card-header">Dokumente hochladen</span>
    """, unsafe_allow_html=True)
    st.info("💡 Dokumente oder Fotos können Sie ganz einfach direkt mit Ihrer Smartphone-Kamera aufnehmen.")
    
    st.write("") # Abstandhalter
    police = st.file_uploader("Letzte Versicherungspolice hier hochladen/fotografieren *", type=["pdf", "png", "jpg", "jpeg"])
    
    # Führerschein: Zwei Spalten nebeneinander
    st.markdown("<p style='color: #0b4aa0; font-weight: bold; margin-bottom: 2px;'>Führerschein aller berechtigten Fahrer *</p>", unsafe_allow_html=True)
    col_fs1, col_fs2 = st.columns(2)
    with col_fs1:
        fs_vorderseite = st.file_uploader("Vorderseite (Pflicht) *", type=["pdf", "png", "jpg", "jpeg"], key="fs_vorn")
    with col_fs2:
        fs_rueckseite = st.file_uploader("Rückseite (Pflicht) *", type=["pdf", "png", "jpg", "jpeg"], key="fs_hinten")
        
    # Personalausweis / Reisepass: Zwei Spalten nebeneinander
    st.markdown("<p style='color: #0b4aa0; font-weight: bold; margin-top: 15px; margin-bottom: 2px;'>Ausweisdokument aller berechtigten Fahrer *</p>", unsafe_allow_html=True)
    col_id1, col_id2 = st.columns(2)
    with col_id1:
        ausweis_vorderseite = st.file_uploader("Vorderseite / Reisepass-Hauptseite *", type=["pdf", "png", "jpg", "jpeg"], key="ausweis_vorn")
    with col_id2:
        ausweis_rueckseite = st.file_uploader("Rückseite (Optional)", type=["pdf", "png", "jpg", "jpeg"], key="ausweis_hinten")
        
    st.markdown('</div>', unsafe_allow_html=True)

    # Pflichtfelder prüfen
    pflichtfelder_ausgefuellt = (name and vorname and geburtsort and fahrzeugschein and police 
                                 and fs_vorderseite and fs_rueckseite and ausweis_vorderseite)

    if pflichtfelder_ausgefuellt:
        if st.button("DATEN JETZT SICHER ÜBERTRAGEN", type="primary"):
            
            # Ordnerstruktur erstellen
            ordner_name = f"Kunde_{name}_{vorname}"
            if not os.path.exists(ordner_name):
                os.makedirs(ordner_name)
            
            # Dateien speichern
            if police:
                with open(os.path.join(ordner_name, f"Police_{police.name}"), "wb") as f:
                    f.write(police.getbuffer())
                    
            if fahrzeugschein:
                with open(os.path.join(ordner_name, f"Fahrzeugschein_{fahrzeugschein.name}"), "wb") as f:
                    f.write(fahrzeugschein.getbuffer())
            
            if fs_vorderseite:
                with open(os.path.join(ordner_name, f"FS_Vorderseite_{fs_vorderseite.name}"), "wb") as f:
                    f.write(fs_vorderseite.getbuffer())
                    
            if fs_rueckseite:
                with open(os.path.join(ordner_name, f"FS_Rueckseite_{fs_rueckseite.name}"), "wb") as f:
                    f.write(fs_rueckseite.getbuffer())

            if ausweis_vorderseite:
                with open(os.path.join(ordner_name, f"Ausweis_Vorderseite_{ausweis_vorderseite.name}"), "wb") as f:
                    f.write(ausweis_vorderseite.getbuffer())
                    
            if ausweis_rueckseite:
                with open(os.path.join(ordner_name, f"Ausweis_Rueckseite_{ausweis_rueckseite.name}"), "wb") as f:
                    f.write(ausweis_rueckseite.getbuffer())

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
        st.warning("⚠️ Bitte füllen Sie alle mit * markierten Felder aus und laden Sie die Pflichtdokumente hoch, um die Übertragung zu starten.")

    # 6. STIMMUNGSBILD GANZ UNTEN
    THEME_BILD = "pg-finance-theme.jpg"
    if os.path.exists(THEME_BILD):
        theme_img = Image.open(THEME_BILD)
        st.image(theme_img, use_container_width=True)

else:
    if pin_eingabe != "":
        st.error("❌ Falsche PIN. Bitte prüfen Sie Ihre Eingabe.")
