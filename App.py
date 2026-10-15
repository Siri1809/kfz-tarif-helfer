import streamlit as st
import os
import requests
import pandas as pd
import zipfile
from PIL import Image
from io import BytesIO

# 1. Seiteneinstellungen
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
            return response.json().get("access_token"), None
        else:
            return None, f"Auth-Fehler ({response.status_code}): {response.json().get('error_description')}"
    except Exception as e:
        return None, f"Verbindungsfehler: {e}"

def read_excel_from_onedrive(token):
    try:
        url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/drive/root:/PG_Finance_Tarifrechner/kunden_pins.xlsx:/content"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            df = pd.read_excel(BytesIO(response.content))
            datenbank = {}
            for _, row in df.iterrows():
                pin = str(row["PIN"]).strip()
                datenbank[pin] = {
                    "nachname": str(row["Nachname"]).strip(),
                    "vorname": str(row["Vorname"]).strip(),
                    "status": str(row.get("Status", "Bereit")).strip()
                }
            return datenbank, None
        elif response.status_code == 404:
            return {}, "404"
        else:
            return {}, f"Fehler ({response.status_code})"
    except Exception as e:
        return {}, f"Exception: {e}"

def upload_file_to_onedrive(token, folder_name, file_name, file_content):
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/drive/root:/PG_Finance_Tarifrechner/{folder_name}/{file_name}:/content"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream"
    }
    requests.put(url, headers=headers, data=file_content)

def update_excel_status_on_onedrive(token, pin_to_update):
    try:
        url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/drive/root:/PG_Finance_Tarifrechner/kunden_pins.xlsx:/content"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            df = pd.read_excel(BytesIO(response.content))
            df.loc[df["PIN"].astype(str) == str(pin_to_update), "Status"] = "Ausgefüllt"
            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False)
            output.seek(0)
            requests.put(url, headers=headers, data=output.getvalue())
    except Exception as e:
        pass

# Token und Datenbank generieren
token, auth_error = get_onedrive_token()
KUNDEN_DATENBANK = {}
excel_error = None

if token:
    KUNDEN_DATENBANK, excel_error = read_excel_from_onedrive(token)

is_using_backup = False
if not KUNDEN_DATENBANK:
    is_using_backup = True
    KUNDEN_DATENBANK = {
        "pgffe": {"nachname": "Geck", "vorname": "Ramona", "status": "Bereit"},
        "011026": {"nachname": "Truetsch", "vorname": "Tobias", "status": "Bereit"},
        "0000": {"nachname": "Seyschab", "vorname": "Simon", "status": "Bereit"},
        "1234": {"nachname": "Grellner", "vorname": "Patrick", "status": "Bereit"},
        "mf1026": {"nachname": "Filip", "vorname": "Markus", "status": "Bereit"}
    }

# CSS (Unverändert)
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
    [data-testid="stFileUploaderDropzone"] {
        border: 2px dashed #00aeeb !important;
        background-color: #f7fafc !important;
        border-radius: 8px !important;
        padding: 15px !important;
        box-shadow: none !important;
        transition: all 0.3s ease !important;
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

st.markdown("<h1 class='main-title'>Datenerfassung</h1>", unsafe_allow_html=True)
st.markdown("<p class='main-subtitle'>Schnell und sicher alle Daten für Ihre Autoversicherung einreichen</p>", unsafe_allow_html=True)

# 4. Sicherheits-Schranke
st.markdown("""
        <div class="form-card">
            <span class="card-header">Zugang freischalten</span>
    """, unsafe_allow_html=True)
pin_eingabe = st.text_input("PIN-Eingabe", type="password", label_visibility="collapsed", placeholder="Bitte Ihre persönliche Kunden-PIN eingeben...")
st.markdown('</div>', unsafe_allow_html=True)

if pin_eingabe in KUNDEN_DATENBANK and KUNDEN_DATENBANK[pin_eingabe].get("status", "Bereit") == "Bereit":
    kunden_info = KUNDEN_DATENBANK[pin_eingabe]
    kunden_nachname = kunden_info["nachname"]
    kunden_vorname = kunden_info["vorname"]

    st.success(f"🔓 Willkommen {kunden_vorname} {kunden_nachname}!")

    # === KARTE 1: PERSÖNLICHE DATEN ===
    st.markdown('<div class="form-card"><span class="card-header">Persönliche Daten</span>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Nachname *", value=kunden_nachname, disabled=True)
        vorname = st.text_input("Vorname *", value=kunden_vorname, disabled=True)
    with col2:
        geburtsort = st.text_input("Geburtsort *")
        familienstand = st.selectbox("Familienstand", ["Ledig", "Verheiratet", "Eingetragene Lebenspartnerschaft", "Geschieden", "Verwitwet"])
    st.markdown('</div>', unsafe_allow_html=True)

    # === KARTE 2: FAHRZEUG ===
    st.markdown('<div class="form-card"><span class="card-header">Fahrzeug & Nutzung</span>', unsafe_allow_html=True)
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

    # === KARTE 3: DOKUMENTE ===
    st.markdown('<div class="form-card"><span class="card-header">Dokumente hochladen</span>', unsafe_allow_html=True)
    st.info("💡 Dokumente oder Fotos können Sie ganz einfach direkt mit Ihrer Smartphone-Kamera aufnehmen.")
    police = st.file_uploader("Letzte Versicherungspolice hier hochladen/fotografieren *", type=["pdf", "png", "jpg", "jpeg"])
    
    st.markdown("<p style='color: #0b4aa0; font-weight: bold; margin-bottom: 2px;'>Führerschein aller berechtigten Fahrer *</p>", unsafe_allow_html=True)
    col_fs1, col_fs2 = st.columns(2)
    with col_fs1:
        fs_vorderseite = st.file_uploader("Vorderseite (Pflicht) *", type=["pdf", "png", "jpg", "jpeg"], key="fs_vorn")
    with col_fs2:
        fs_rueckseite = st.file_uploader("Rückseite (Pflicht) *", type=["pdf", "png", "jpg", "jpeg"], key="fs_hinten")
        
    st.markdown("<p style='color: #0b4aa0; font-weight: bold; margin-top: 15px; margin-bottom: 2px;'>Ausweisdokument aller berechtigten Fahrer *</p>", unsafe_allow_html=True)
    col_id1, col_id2 = st.columns(2)
    with col_id1:
        ausweis_vorderseite = st.file_uploader("Vorderseite / Reisepass-Hauptseite *", type=["pdf", "png", "jpg", "jpeg"], key="ausweis_vorn")
    with col_id2:
        ausweis_rueckseite = st.file_uploader("Rückseite (Optional)", type=["pdf", "png", "jpg", "jpeg"], key="ausweis_hinten")
    st.markdown('</div>', unsafe_allow_html=True)

    pflicht_kennzeichen = neufahrzeug or (kennzeichen and kennzeichen != "")
    pflichtfelder_ausgefuellt = (name and vorname and geburtsort and fahrzeugschein and police 
                                 and fs_vorderseite and fs_rueckseite and ausweis_vorderseite and pflicht_kennzeichen)

    if pflichtfelder_ausgefuellt:
        if st.button("DATEN JETZT SICHER ÜBERTRAGEN", type="primary"):
            safe_kz = kennzeichen.replace(" ", "-").replace("/", "-")
            ordner_name = f"Kunde_{name}_{vorname}_{safe_kz}"
            
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

            # Dateispeicherung
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

            if token:
                with st.spinner("Dateien werden auf Ihr OneDrive geladen..."):
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
                    update_excel_status_on_onedrive(token, pin_eingabe)
                st.balloons()
                st.success("🎉 Übertragung auf OneDrive erfolgreich!")
            else:
                st.balloons()
                st.success("🎉 Übertragung erfolgreich! (Sicher lokal gespeichert)")

            st.write("---")
            st.subheader("📋 Kopierbereich")
            st.code(infotext, language="text")

    THEME_BILD = "pg-finance-theme.jpg"
    if os.path.exists(THEME_BILD):
        st.image(Image.open(THEME_BILD), use_container_width=True)

# =========================================================================
# 📋 GEHEIMER DOWNLOAD-BEREICH FÜR DEN MAKLER (NUR SICHTBAR FÜR PIN '1234')
# =========================================================================
if pin_eingabe == "1234":
    st.write("---")
    st.subheader("📁 Backup-Daten-Manager (Nur für Sie sichtbar)")
    st.info("Hier können Sie alle lokal auf dem Server gespeicherten Kundenordner einsehen und als ZIP-Archiv herunterladen.")
    
    # Listet alle Ordner auf dem Server auf, die mit "Kunde_" anfangen
    lokale_ordner = [d for d in os.listdir('.') if os.path.isdir(d) and d.startswith("Kunde_")]
    
    if lokale_ordner:
        ausgewaehlter_ordner = st.selectbox("Wählen Sie einen Kundenordner zum Herunterladen:", lokale_ordner)
        
        if ausgewaehlter_ordner:
            # Erstellt ein ZIP-Archiv im Speicher
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                for root, dirs, files in os.walk(ausgewaehlter_ordner):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zip_file.write(file_path, os.path.relpath(file_path, ausgewaehlter_ordner))
            
            # Download-Button für das ZIP
            st.download_button(
                label=f"💾 Ordner '{ausgewaehlter_ordner}' als ZIP herunterladen",
                data=zip_buffer.getvalue(),
                file_name=f"{ausgewaehlter_ordner}.zip",
                mime="application/zip"
            )
    else:
        st.write("Keine lokalen Kundenordner auf dem Server vorhanden.")
# =========================================================================
