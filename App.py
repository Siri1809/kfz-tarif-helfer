import streamlit as st
import os
from PIL import Image

# 1. Seiteneinstellungen
st.set_page_config(
    page_title="Tarifrechner Helfer - Patrick Grellner Finance", 
    page_icon="🚗", 
    layout="centered"
)

# Initialisierung des Session State für die Fahreranzahl
if 'driver_count' not in st.session_state:
    st.session_state.driver_count = 1

# 2. Überarbeitetes CSS für ein stabiles Design
st.markdown("""
<style>
    /* Grundlegende App-Styles */
    .stApp {
        background-color: #ffffff !important;
        color: #2d3748 !important;
        font-family: 'Varela Round', 'Varela', sans-serif !important;
    }
    .main-title {
        font-family: 'Varela Round', sans-serif; color: #0b4aa0; font-weight: 700;
        font-size: 2.2rem; text-align: center; margin-top: 10px; margin-bottom: 5px;
    }
    .main-subtitle {
        text-align: center; color: #718096; font-size: 1.1rem; margin-bottom: 20px;
    }
    .form-card {
        background-color: #ffffff; padding: 24px; border-radius: 12px;
        border: 1px solid #edf2f7; margin-bottom: 20px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
    }
    .section-title {
        color: #0b4aa0; font-size: 1.3rem; font-weight: 600; margin-bottom: 18px;
        border-bottom: 2px solid #00aeeb; padding-bottom: 8px;
    }
    label {
        color: #0b4aa0 !important; font-weight: bold !important;
        font-size: 0.95rem !important; margin-bottom: 6px !important;
    }

    /* --- FINALE KORREKTUR FÜR ALLE EINGABEFELDER --- */

    /* Standard Text- & Nummern-Eingabefelder */
    .stTextInput input, .stNumberInput input {
        background-color: #ffffff !important;
        color: #0b4aa0 !important;
        border: 2px solid #00aeeb !important;
        border-radius: 6px !important;
        padding: 10px 14px !important;
        font-family: 'Varela Round', sans-serif !important;
        font-weight: bold !important;
        transition: all 0.2s ease-in-out !important;
    }

    /* Dropdown-Menü (Selectbox) */
    div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border: 2px solid #00aeeb !important;
        border-radius: 6px !important;
        font-family: 'Varela Round', sans-serif !important;
        font-weight: bold !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #0b4aa0 !important;
        font-weight: bold !important;
    }
    div[data-baseweb="select"] > div > div {
        color: #0b4aa0 !important;
    }

    /* Hover & Focus Effekte für alle Felder */
    .stTextInput input:hover, .stNumberInput input:hover, div[data-baseweb="select"]:hover {
        border-color: #0b4aa0 !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus, div[data-baseweb="select"]:focus-within {
        border-color: #0b4aa0 !important;
        box-shadow: 0 0 0 3px rgba(11, 74, 160, 0.2) !important;
    }

    /* --- ÜBERARBEITETES DESIGN FÜR FILE UPLOADER --- */
    [data-testid="stFileUploader"] {
        border: 2px dashed #00aeeb;
        border-radius: 6px;
        padding: 20px;
        text-align: center;
        background-color: #f7fcff;
    }
    [data-testid="stFileUploader"] label {
        color: #0b4aa0 !important;
        font-size: 1rem !important;
    }
    [data-testid="stFileUploader"] button {
        border: none;
        background-color: #00aeeb;
        color: white;
        border-radius: 6px;
        padding: 8px 16px;
    }
    [data-testid="stFileUploader"] button:hover {
        background-color: #0b4aa0;
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
        box-shadow: 0 4px 14px rgba(0, 174, 235, 0.2) !important;
        margin-bottom: 20px !important;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #0b4aa0 !important;
        box-shadow: 0 6px 20px rgba(11, 74, 160, 0.3) !important;
        transform: translateY(-1px);
    }

    /* --- SUB-HEADER FÜR DYNAMISCHE FAHRER --- */
    .driver-header {
        font-size: 1.1rem;
        font-weight: bold;
        color: #0b4aa0;
        margin-top: 20px;
        margin-bottom: 10px;
        border-top: 1px solid #edf2f7;
        padding-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Logo & Titel
LOGO_DATEINAME = "pg-finance_Logo.jpg"
if os.path.exists(LOGO_DATEINAME):
    logo = Image.open(LOGO_DATEINAME)
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.image(logo, use_container_width=True)
else:
    st.markdown("<h2 style='text-align: center;'>PATRICK GRELLNER FINANCE</h2>", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>Datenerfassung</h1>", unsafe_allow_html=True)
st.markdown("<p class='main-subtitle'>Schnell und sicher alle Daten für Ihre Autoversicherung einreichen</p>", unsafe_allow_html=True)

# 4. PIN-Eingabe
KORREKTE_PIN = "1234"
with st.container():
    st.markdown("<div class='form-card'><h3 style='font-size: 1.1rem; margin-bottom: 12px;'>🔑 Zugang freischalten</h3>", unsafe_allow_html=True)
    pin_eingabe = st.text_input("PIN-Eingabe", type="password", label_visibility="collapsed", placeholder="Bitte PIN eingeben...")
    st.markdown("</div>", unsafe_allow_html=True)

if pin_eingabe == KORREKTE_PIN:
    st.success("🔓 Zugang erfolgreich freigeschaltet.")

    with st.container():
        st.markdown("<div class='form-card'><div class='section-title'>👤 Persönliche Daten</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Nachname *")
            vorname = st.text_input("Vorname *")
        with col2:
            geburtsort = st.text_input("Geburtsort *")
            familienstand = st.selectbox("Familienstand", ["Ledig", "Verheiratet", "Eingetragene Lebenspartnerschaft", "Geschieden", "Verwitwet"])
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='form-card'><div class='section-title'>🚘 Fahrzeug & Nutzung</div>", unsafe_allow_html=True)
        fahrleistung = st.number_input("Jährliche Fahrleistung (in km) *", value=10000, step=1000)
        km_stand = st.number_input("Aktueller Kilometerstand (bei älteren Fahrzeugen)", value=0, step=5000)
        garage = st.selectbox("Abstellort des Fahrzeugs (Garage) *", ["Einzel-/Doppelgarage", "Tiefgarage", "Carport", "Privatgrundstück (befriedet)", "Straße / Laternenparker"])
        st.markdown('</div>', unsafe_allow_html=True)

    # === ÜBERARBEITETER DOKUMENTEN-UPLOAD ===
    with st.container():
        st.markdown("<div class='form-card'><div class='section-title'>📂 Dokumente hochladen</div>", unsafe_allow_html=True)
        st.info("💡 Dokumente oder Fotos können Sie ganz einfach direkt mit Ihrer Smartphone-Kamera aufnehmen.")
        
        st.subheader("Letzte Versicherungspolice")
        police = st.file_uploader("Police oder letzte Beitragsrechnung *", type=["pdf", "png", "jpg", "jpeg"], key="police")

        # Dynamische Upload-Felder für Fahrer
        uploaded_files = {'fuehrerscheine': [], 'ausweise': []}
        all_driver_docs_uploaded = True

        for i in range(st.session_state.driver_count):
            driver_num = i + 1
            st.markdown(f"<div class='driver-header'>Fahrer {driver_num}</div>", unsafe_allow_html=True)

            st.subheader("Führerschein")
            fs_col1, fs_col2 = st.columns(2)
            with fs_col1:
                fs_vorder = st.file_uploader(f"Vorderseite 📎", key=f"fs_vorder_{driver_num}")
            with fs_col2:
                fs_rueck = st.file_uploader(f"Rückseite 📎", key=f"fs_rueck_{driver_num}")

            st.subheader("Personalausweis")
            pa_col1, pa_col2 = st.columns(2)
            with pa_col1:
                pa_vorder = st.file_uploader(f"Vorderseite 📎", key=f"pa_vorder_{driver_num}")
            with pa_col2:
                pa_rueck = st.file_uploader(f"Rückseite 📎", key=f"pa_rueck_{driver_num}")

            # Nur für den ersten Fahrer ist der Upload Pflicht
            if driver_num == 1 and not (fs_vorder and fs_rueck and pa_vorder and pa_rueck):
                all_driver_docs_uploaded = False
            
            if fs_vorder: uploaded_files['fuehrerscheine'].append(fs_vorder)
            if fs_rueck: uploaded_files['fuehrerscheine'].append(fs_rueck)
            if pa_vorder: uploaded_files['ausweise'].append(pa_vorder)
            if pa_rueck: uploaded_files['ausweise'].append(pa_rueck)

        # Button zum Hinzufügen weiterer Fahrer nur anzeigen, wenn alle Dokumente des aktuellen Fahrers hochgeladen sind
        if all_driver_docs_uploaded:
            if st.button("Weiteren Fahrer hinzufügen"):
                st.session_state.driver_count += 1
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # Pflichtfelder prüfen
    pflichtfelder_ausgefuellt = name and vorname and geburtsort and police and all_driver_docs_uploaded

    if pflichtfelder_ausgefuellt:
        if st.button("DATEN JETZT SICHER ÜBERTRAGEN", type="primary"):
            # ... Ihre Logik zum Speichern der Daten ...
            st.balloons()
            st.success("🎉 Übertragung erfolgreich! Ihre Daten wurden sicher an uns übermittelt.")
    else:
        st.warning("⚠️ Bitte füllen Sie alle mit * markierten Felder aus und laden Sie die Pflicht-Dokumente hoch, um die Übertragung zu starten.")

    # 6. STIMMUNGSBILD GANZ UNTEN (WIEDER EINGEFÜGT)
    THEME_BILD = "pg-finance-theme.jpg"
    if os.path.exists(THEME_BILD):
        theme_img = Image.open(THEME_BILD)
        st.image(theme_img, use_container_width=True)

else:
    if pin_eingabe != "":
        st.error("❌ Falsche PIN. Bitte prüfen Sie Ihre Eingabe.")
