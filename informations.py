import pymongo
import streamlit as st
import time
from database import MongoDB

db = MongoDB()


class information:
    def __init__(self):
        st.set_page_config(page_title="YeltaCare",
                           page_icon="❤️", layout="centered")

        st.markdown(
            "<h1 style='text-align: center; color: #FF4B4B;'>🩺 Formulaire de Santé</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: gray;'>Remplissez ce formulaire pour obtenir une analyse rapide de votre santé.</h4>", unsafe_allow_html=True)
        st.divider()

        # --- FORMULAIRE ---
        with st.form("health_form"):
            st.subheader("👤 Informations Générales")

            col1, col2 = st.columns(2)
            with col1:
                nom = st.text_input("Nom", placeholder="Entrez votre nom ici")
            with col2:
                age = st.slider("Âge", 0, 100, 25)

            genre = st.radio(
                "Genre", ["Homme", "Femme", "Autre"], horizontal=True)

            col1, col2 = st.columns(2)
            with col1:
                taille = st.slider("Taille (cm)", 100, 220, 170)
            with col2:
                poids = st.slider("Poids (kg)", 30, 200, 70)

            st.subheader("🏃 Mode de Vie")
            activite_physique = st.select_slider("Niveau d'activité physique",
                                                 options=["Sédentaire", "Légère", "Modérée", "Intense"])
            sommeil = st.slider("🛏️ Heures de sommeil par nuit", 3, 12, 7)
            stress = st.slider("😰 Niveau de stress", 1, 10, 5)

            st.subheader("🥗 Habitudes Alimentaires")
            alimentation = st.multiselect("🍽️ Types d'aliments consommés régulièrement",
                                          ["🥦 Fruits & Légumes", "🥩 Viande & Poisson", "🥛 Produits laitiers",
                                           "🍞 Céréales & Féculents", "🍔 Fast-food", "🥤 Boissons sucrées"])
            eau = st.slider("💧 Litres d'eau consommés par jour",
                            0.5, 5.0, 2.0, step=0.1)

            st.subheader("🩺 Antécédents Médicaux")
            antecedents = st.text_area(
                "📜 Antécédents médicaux", placeholder="Ex : diabète, hypertension...")
            fumeur = st.radio(
                "🚬 Fumez-vous ?", ["Non", "Occasionnellement", "Régulièrement"], horizontal=True)
            alcool = st.radio("🍷 Consommez-vous de l'alcool ?",
                              ["Jamais", "Rarement", "Régulièrement"], horizontal=True)

            submit_button = st.form_submit_button("📩 Soumettre")

        if submit_button:
            # Calcul de l'IMC
            imc = round(poids / ((taille / 100) ** 2), 2)

            # Création du JSON pour MongoDB
            user_data = {
                "nom": nom,
                "age": age,
                "genre": genre,
                "taille_cm": taille,
                "poids_kg": poids,
                "IMC": imc,
                "activite_physique": activite_physique,
                "sommeil_h": sommeil,
                "stress_niveau": stress,
                "alimentation": alimentation,
                "eau_L": eau,
                "antecedents_medicaux": antecedents,
                "fumeur": fumeur,
                "alcool": alcool,
                "date_enregistrement": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            db.set_collection("Infos")
            db.insert_data(user_data)
            st.success(
                f"✅ Profil de santé de {nom} enregistré avec succès!")

            # time.sleep(2)
            # st.switch_page("principal")  # Redirection après sauvegarde
