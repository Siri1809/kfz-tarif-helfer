import streamlit as st
import os
import requests
import pandas as pd
from PIL import Image
from io import BytesIO

# 1. Seiteneinstellungen
st.set_page_config(
    page_title="Tarifrechner Helfer - Patrick Grellner Finance", 
    page_icon="🚗", 
    layout="centered"
)

# === MICROSOFT GRAPH API VERBINDUNG (DIAGNOSE-MODUS) ===
try:
    CLIENT_ID = st.secrets["microsoft"]["client_id"]
    CLIENT_SECRET = st.secrets["microsoft"]["client_secret"]
    TENANT_ID = st.secrets["microsoft"]["tenant_id"]
except Exception:
    st.error("🔑 Die Microsoft-Schlüssel fehlen im Streamlit-Tresor. Bitte tragen Sie diese in den Secrets ein!")
    CLIENT_ID, CLIENT_SECRET, TENANT_ID = None, None, None

def get_onedrive_token():
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
    return None

# Token generieren
token = get_onedrive_token()

st.title("🔍 OneDrive Verbindungs-Diagnose")
st.write("Wir testen jetzt die Verbindung zu Ihrem OneDrive, um den exakten Fehler zu finden.")

if token:
    st.success("✅ Verbindung zu Microsoft erfolgreich hergestellt (Token generiert)!")
    
    # TEST 1: Versuchen, den App-Pfad abzufragen
    url_test = "https://graph.microsoft.com/v1.0/me/drive/special/approot"
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url_test, headers=headers)
    
    st.write("---")
    st.subheader("Ergebnis der OneDrive-Abfrage:")
    
    if res.status_code == 200:
        st.success("🎉 Microsoft hat den App-Ordner freigegeben!")
        # Zeigt den echten Pfad an, den Microsoft für diese App reserviert hat
        path_info = res.json().get("parentReference", {}).get("path", "")
        st.info(f"Der exakte Pfad auf Ihrem OneDrive lautet laut Microsoft:\n`{path_info}`")
    else:
        st.error(f"❌ Microsoft verweigert den Zugriff auf den App-Ordner (Fehlercode {res.status_code}).")
        st.write("Detaillierte Fehlermeldung von Microsoft:")
        st.code(res.text)
else:
    st.error("❌ Verbindung zu Microsoft fehlgeschlagen. Bitte prüfen Sie Ihre Schlüssel im Streamlit-Tresor!")
