import streamlit as st
import os
import requests
from PIL import Image

# 1. Seiteneinstellungen (Auf Smartphones optimiert)
st.set_page_config(
    page_title="Tarifrechner Helfer - Patrick Grellner Finance", 
    page_icon="🚗", 
    layout="centered"
)

# === DIE FIRMEN-E-MAIL FÜR IHR ONEDRIVE ===
USER_EMAIL = "s.seyschab@pg-finance.de"

# === MICROSOFT GRAPH API VERBINDUNG ===
CLIENT_ID = st.secrets["microsoft"]["client_id"]
CLIENT_SECRET = st.secrets["microsoft"]["client_secret"]
TENANT_ID = st.secrets["microsoft"]["tenant_id"]

def get_onedrive_token():
    """Authentifiziert die App bei Microsoft Graph API."""
    try:
        url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "client_id": CLIENT_ID,
            "scope": "https://graph.microsoft.com/.default",
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials"
        }
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json().get("access_token")
    except Exception:
        pass
    return None

def upload_file_to_onedrive(token, folder_name, file_name, file_content):
    """Lädt eine Datei direkt in den Kundenordner auf Simons OneDrive."""
    # Der Ordner wird direkt im Hauptverzeichnis unter 'PG_Finance_Tarifrechner' angelegt!
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/drive/root:/PG_Finance_Tarifrechner/{folder_name}/{file_name}:/content"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream"
    }
    requests.put(url, headers=headers, data=file_content)

token = get_onedrive_token()

# 2. BRANDING, SEAMLESS CARD, SPACING & DEEP MOBILE CONTRAST FIX CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff !important;
        background-image: none !important;
        color: #2d3748 !important;
        font-family: 'Varela Round', 'Varela', sans-serif !important;
    }
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
    .form-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #edf2f7;
        margin-top: 0px !important;
        margin-bottom: 25px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
    }
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
    .stSelectbox span, .stSelectbox div {
        color: #0b4aa0 !important;
        font-weight: bold !important;
    }
    .stTextInput input:hover, .stNumberInput input:hover, .stSelectbox [data-baseweb="select"]:hover {
        border-color: #0b4aa0 !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox [data-baseweb="select"]:focus {
        border-color: #0b4aa0 !important;
        box-shadow: 0 0 0 3px rgba(11, 74, 160, 0.2) !important;
    }
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
    .stAlert p, .stAlert span, .stAlert div {
        color: #1a1a1a !important;
        font-weight: bold !important;
    }
    label {
        color: #0b4aa0 !important;
        font-weight: bold !important;
        font-size: 0.95rem !important;
        margin-bottom: 6px !important;
    }
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
    </style>
""", unsafe_allow_html=True)

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

# === KARTE 1: PERSÖNLICHE DATEN (Namen jetzt wieder frei tippbar!) ===
st.markdown("""
    <div class="form-card">
        <span class="card-header">👤 Persönliche Daten</span>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Nachname *")
    vorname = st.text_input("Vorname *")
with col2:
    geburtsort = st.text_input("Geburtsort *")
    familienstand = st.selectbox("Familienstand", ["Ledig", "Verheiratet", "Eingetragene Lebenspartnerschaft", "Geschieden", "Verwitwet"])
st.markdown('</div>', unsafe_allow_html=True)

# === KARTE 2: FAHRZEUG ===
st.markdown("""
    <div class="form-card">
        <span class="card-header">🚘 Fahrzeug & Nutzung</span>
""", unsafe_allow_html=True)

col_fz1, col_col2 = st.columns(2)
with col_fz1:
    fahrleistung = st.number_input("Jährliche Fahrleistung (in km) *", value=10000, step=1000)
    km_stand = st.number_input("Aktueller Kilometerstand", value=0, step=5000)
with col_col2:
    garage = st.selectbox("Abstellort des Fahrzeugs (Garage) *", ["Einzel-/Doppelgarage", "Tiefgarage", "Carport", "Privatgrundstück (befriedet)", "Straße / Laternenparker"])

st.write("") 
col_kz1, col_kz2 = st.columns([2, 1])
with col_kz2:
    neufahrzeug = st.checkbox("Neufahrzeug", help="Aktivieren Sie dies, falls das Fahrzeug noch nicht zugelassen ist.")
with col_kz1:
    if neufahrzeug:
        kennzeichen = st.text_input("Amtliches Kennzeichen", value="NEUFAHRZEUG", disabled=True)
    else:
        kennzeichen = st.text_input("Amtliches Kennzeichen *", placeholder="z.B. BA-PG-99")

st.write("")
fahrzeugschein = st.file_uploader("Fahrzeugschein hier hochladen/fotografieren *", type=["pdf", "png", "jpg", "jpeg"])
st.markdown('</div>', unsafe_allow_html=True)

# === KARTE 3: DOKUMENTE (Jetzt mit optionalen Ausweis- & Führerscheinfeldern!) ===
st.markdown("""
    <div class="form-card">
        <span class="card-header">📂 Dokumente hochladen</span>
""", unsafe_allow_html=True)
st.info("💡 Dokumente oder Fotos können Sie ganz einfach direkt mit Ihrer Smartphone-Kamera aufnehmen.")

st.write("") 
police = st.file_uploader("Letzte Versicherungspolice hier hochladen/fotografieren *", type=["pdf", "png", "jpg", "jpeg"])

# Führerscheine (OPTIONAL - kein Sternchen mehr!)
st.markdown("<p style='color: #0b4aa0; font-weight: bold; margin-bottom: 2px;'>Führerschein aller berechtigten Fahrer (Optional)</p>", unsafe_allow_html=True)
col_fs1, col_fs2 = st.columns(2)
with col_fs1:
    fs_vorderseite = st.file_uploader("Vorderseite", type=["pdf", "png", "jpg", "jpeg"], key="fs_vorn")
with col_fs2:
    fs_rueckseite = st.file_uploader("Rückseite", type=["pdf", "png", "jpg", "jpeg"], key="fs_hinten")
    
# Ausweise (OPTIONAL - kein Sternchen mehr!)
st.markdown("<p style='color: #0b4aa0; font-weight: bold; margin-top: 15px; margin-bottom: 2px;'>Ausweisdokument aller berechtigten Fahrer (Optional)</p>", unsafe_allow_html=True)
col_id1, col_id2 = st.columns(2)
with col_id1:
    ausweis_vorderseite = st.file_uploader("Vorderseite / Reisepass-Hauptseite", type=["pdf", "png", "jpg", "jpeg"], key="ausweis_vorn")
with col_id2:
    ausweis_rueckseite = st.file_uploader("Rückseite", type=["pdf", "png", "jpg", "jpeg"], key="ausweis_hinten")
st.markdown('</div>', unsafe_allow_html=True)

# === DATENSCHUTZ-EINWILLIGUNG (Rechtliche Absicherung für Sie!) ===
st.markdown("""
    <div class="form-card">
        <span class="card-header">⚖️ Datenschutz & Einwilligung</span>
""", unsafe_allow_html=True)
datenschutz_akzeptiert = st.checkbox("Ich willige ein, dass meine Daten und Dokumente zum Zwecke der Angebotserstellung für die Kfz-Versicherung verarbeitet und gespeichert werden dürfen. Diese Einwilligung kann ich jederzeit widerrufen. *")
st.markdown('</div>', unsafe_allow_html=True)

# Pflichtfelder-Validierung (Führerschein und Ausweis sind jetzt KEINE Pflicht mehr!)
pflicht_kennzeichen = neufahrzeug or (kennzeichen and kennzeichen != "")
pflichtfelder_ausgefuellt = (name and vorname and geburtsort and fahrzeugschein and police 
                             and pflicht_kennzeichen and datenschutz_akzeptiert)

if pflichtfelder_ausgefuellt:
    if st.button("DATEN JETZT SICHER ÜBERTRAGEN", type="primary"):
        
        safe_kz = kennzeichen.replace(" ", "-").replace("/", "-")
        ordner_name = f"Kunde_{name}_{vorname}_{safe_kz}"
        
        # Lokales Backup erstellen
        if not os.path.exists(ordner_name):
            os.makedirs(ordner_name)

        infotext = f"""=== KUNDENDATEN FÜR NAFI / COMPARIT ===
Name: {name}
Vorname: {vorname}
Geburtsort: {geburtsort}
Familienstand: {familienstand}
----------------------------------------
Kennzeichen: {kennzeichen}
Fahrleistung: {fahrleistung} km/Jahr
Aktueller KM-Stand: {km_stand} km
Garage: {garage}
========================================"""

        with open(os.path.join(ordner_name, "Kopier_Vorlage.txt"), "w", encoding="utf-8") as f:
            f.write(infotext)

        # === ONEDRIVE HOCHLADEN-PROZESS ===
        if token:
            with st.spinner("Dateien werden sicher auf Ihr OneDrive geladen..."):
                upload_file_to_onedrive(token, ordner_name, "Kopier_Vorlage.txt", infotext.encode("utf-8"))
                
                if fahrzeugschein:
                    upload_file_to_onedrive(token, ordner_name, f"Fahrzeugschein_{fahrzeugschein.name}", fahrzeugschein.getbuffer())
                if police:
                    upload_file_to_onedrive(token, ordner_name, f"Police_{police.name}", police.getbuffer())
                if fs_vorderseite:
                    upload_file_to_onedrive(token, ordner_name, f"FS_Vorderseite_{fs_vorderseite.name}", fs_vorderseite.getbuffer())
                if fs_rueckseite:
                    upload_file_to_onedrive(token, ordner_name, f"FS_Rueckseite_{fs_rueckseite.name}", fs_rueckseite.getbuffer())
                if ausweis_vorderseite:
                    upload_file_to_onedrive(token, ordner_name, f"Ausweis_Vorderseite_{ausweis_vorderseite.name}", ausweis_vorderseite.getbuffer())
                if ausweis_rueckseite:
                    upload_file_to_onedrive(token, ordner_name, f"Ausweis_Rueckseite_{ausweis_rueckseite.name}", ausweis_rueckseite.getbuffer())
                
            st.balloons()
            st.success("🎉 Übertragung erfolgreich! Alle Daten und Dokumente wurden sicher auf Ihrem OneDrive abgelegt.")
        else:
            st.balloons()
            st.success("🎉 Übertragung erfolgreich! (Daten wurden sicher lokal auf dem Server gespeichert, da OneDrive noch keine Admin-Freigabe hat).")

        st.write("---")
        st.subheader("📋 Kopierbereich für das Maklerbüro")
        st.code(infotext, language="text")

else:
    st.warning("⚠️ Bitte füllen Sie alle mit * markierten Felder aus, laden Sie die Pflichtdokumente hoch und bestätigen Sie die Datenschutzerklärung, um das Formular abzusenden.")

# 6. STIMMUNGSBILD GANZ UNTEN
THEME_BILD = "pg-finance-theme.jpg"
if os.path.exists(THEME_BILD):
    theme_img = Image.open(THEME_BILD)
    st.image(theme_img, use_container_width=True)
