import streamlit as st
import os
import requests
import pandas as pd
from PIL import Image
from io import BytesIO

# 1. Seiteneinstellungen
st.set_page_config(
    page_title="OneDrive Pfadfinder - Patrick Grellner Finance", 
    page_icon="🔍", 
    layout="centered"
)

# === MICROSOFT GRAPH API VERBINDUNG ===
CLIENT_ID = st.secrets["microsoft"]["client_id"]
CLIENT_SECRET = st.secrets["microsoft"]["client_secret"]
TENANT_ID = st.secrets["microsoft"]["tenant_id"]
USER_EMAIL = "s.seyschab@pg-finance.de"

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
            return None, f"Auth-Fehler: {response.json().get('error_description')}"
    except Exception as e:
        return None, f"Verbindungsfehler: {e}"

token, auth_error = get_onedrive_token()

st.title("🔍 OneDrive Pfadfinder-Diagnose")
st.write("Wir analysieren jetzt die Struktur von Simons OneDrive, um den exakten Pfadnamen zu finden.")

if token:
    st.success("✅ Schritt 1: Erfolgreich bei Microsoft angemeldet!")
    
    # === ANALYSE 1: Hauptverzeichnis abfragen ===
    st.subheader("📁 Analyse der obersten Ebene (Meine Dateien):")
    url_root = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/drive/root/children"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url_root, headers=headers)
    
    if response.status_code == 200:
        items = response.json().get("value", [])
        st.write(f"Es wurden **{len(items)} Ordner/Dateien** auf der obersten Ebene gefunden:")
        
        # Erstellt eine Liste für die Tabelle
        ordner_liste = []
        for item in items:
            typ = "📁 Ordner" if "folder" in item else "📄 Datei"
            name = item.get("name")
            id_val = item.get("id")
            ordner_liste.append({"Typ": typ, "Name (Exakter Systemname)": name, "ID": id_val})
        
        # Zeigt die echten Ordnernamen als schicke Tabelle an
        st.table(pd.DataFrame(ordner_liste))
        
        # Prüfen, ob unser gewünschter Ordner existiert
        suchname = "PG_Finance_Tarifrechner"
        ordner_gefunden = any(x["Name (Exakter Systemname)"] == suchname for x in ordner_liste)
        
        if ordner_gefunden:
            st.success(f"🎯 Der Ordner '{suchname}' wurde im System gefunden!")
            
            # === ANALYSE 2: Inhalt des Ordners abfragen ===
            st.subheader(f"📄 Inhalt des Ordners '{suchname}':")
            url_folder = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/drive/root:/{suchname}:/children"
            res_folder = requests.get(url_folder, headers=headers)
            
            if res_folder.status_code == 200:
                sub_items = res_folder.json().get("value", [])
                if sub_items:
                    st.write(f"Folgende Dateien liegen im Ordner '{suchname}':")
                    for s_item in sub_items:
                        st.code(s_item.get("name"))
                else:
                    st.warning(f"Der Ordner '{suchname}' ist aktuell komplett leer. Bitte laden Sie 'kunden_pins.xlsx' hoch!")
            else:
                st.error(f"Fehler beim Öffnen des Ordners: {res_folder.status_code}")
        else:
            st.error(f"❌ Der Ordner '{suchname}' wurde im System NICHT gefunden.")
            st.info(f"💡 Bitte erstellen Sie im OneDrive einen Ordner mit dem exakten Namen: `{suchname}`")
            
    else:
        st.error(f"❌ Fehler beim Auslesen des Hauptverzeichnisses: {response.status_code}")
        st.code(response.text)
        
else:
    st.error(f"❌ Anmeldung fehlgeschlagen.\n{auth_error}")
