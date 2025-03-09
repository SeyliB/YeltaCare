import streamlit as st
import database

from streamlit_calendar import calendar
from streamlit_extras.metric_cards import style_metric_cards

import pandas as pd

def display():
    st.markdown("<h2 style='text-align: center;'>📊 Votre Profil de Santé</h2>", unsafe_allow_html=True)

    collection = database.getCollection("Informations").get

    col1, col2, col3 = st.columns(3)
    col1.metric("📏 Taille", f"{taille} cm")
    col2.metric("⚖️ Poids", f"{poids} kg")
    col3.metric("📌 IMC", f"{imc}")

    col1, col2, col3 = st.columns(3)
    col1.metric("🏃 Activité", activite_physique)
    col2.metric("💤 Sommeil", f"{sommeil}h")
    col3.metric("💧 Eau", f"{eau} L/jour")

    style_metric_cards()