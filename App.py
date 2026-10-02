import streamlit as st
import os
from PIL import Image

# 1. Seiteneinstellungen (Auf Smartphones optimiert)
st.set_page_config(
    page_title="Tarifrechner Helfer - Patrick Grellner Finance",
    page_icon="🚗",
    layout="centered"
)

# 2. BRANDING & SEAMLESS BORDER CSS (Garantiert eine glatte, durchgezogene Optik für alle Felder)
# ... Ihr CSS-Code bleibt unverändert ...
st.markdown("""
    <style>
    /* ... Ihr gesamter CSS-Code hier ... */
    </style>
""", unsafe_allow_html=True)


# 3. Logo einbinden & zentrieren
# ... Ihr Logo-Code bleibt unverändert ...


st.markdown("<h1 class='main-title'>Datenerfassung</h1>", unsafe_allow_html=True)
st.markdown("<p class='main-subtitle'>Schnell und sicher alle Daten für Ihre Autoversicherung einreichen</p>", unsafe_allow_html=True)

# 4. Sicherheits-Schranke: Die Kunden-PIN
KORREKTE_PIN = "1234"

# Wir verwenden hier einen Container, damit der Abschnitt als eine Einheit behandelt wird
with st.container():
    st.markdown("<h3 style='font-size: 1.1rem; color: #0b4aa0; margin-top: 0; margin-bottom: 12px;'>🔑 Zugang freischalten</h3>", unsafe_allow_html=True)
    pin_eingabe = st.text_input("PIN-Eingabe", type="password", label_visibility="collapsed", placeholder="Bitte PIN eingeben...")


if pin_eingabe == KORREKTE_PIN:
    st.success("🔓 Zugang erfolgreich freigeschaltet.")

    # === KARTE 1: PERSÖNLICHE DATEN ===
    with st.container():
        st.markdown("<div class='section-title'>👤 Persönliche Daten</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Nachname *")
            vorname = st.text_input("Vorname *")
        with col2:
            geburtsort = st.text_input("Geburtsort *")
            familienstand = st.selectbox("Familienstand", ["Ledig", "Verheiratet", "Eingetragene Lebenspartnerschaft", "Geschieden", "Verwitwet"])

    # === KARTE 2: FAHRZEUG ===
    with st.container():
        st.markdown("<div class='section-title'>🚘 Fahrzeug & Nutzung</div>", unsafe_allow_html=True)
        fahrleistung = st.number_input("Jährliche Fahrleistung (in km) *", value=10000, step=1000)
        km_stand = st.number_input("Aktueller Kilometerstand (bei älteren Fahrzeugen)", value=0, step=5000)
        garage = st.selectbox("Abstellort des Fahrzeugs (Garage) *", ["Einzel-/Doppelgarage", "Tiefgarage", "Carport", "Privatgrundstück (befriedet)", "Straße / Laternenparker"])

    # === KARTE 3: DOKUMENTE ===
    with st.container():
        st.markdown("<div class='section-title'>📂 Dokumente hochladen</div>", unsafe_allow_html=True)
        st.info("💡 Dokumente oder Fotos können Sie ganz einfach direkt mit Ihrer Smartphone-Kamera aufnehmen.")
        police = st.file_uploader("Letzte Versicherungspolice *", type=["pdf", "png", "jpg", "jpeg"])
        fuehrerscheine = st.file_uploader("Führerschein Vorder- & Rückseite (aller Fahrer) *", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
        ausweise = st.file_uploader("Personalausweis Vorder- & Rückseite (aller Fahrer) *", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)


    # ... Der Rest Ihres Codes für die Datenverarbeitung bleibt unverändert ...

else:
    if pin_eingabe != "":
        st.error("❌ Falsche PIN. Bitte prüfen Sie Ihre Eingabe.")

# ... Der Rest Ihres Codes bleibt unverändert ...
