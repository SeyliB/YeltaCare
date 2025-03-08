import streamlit as st

class information:
    def __init__(self):
        """Initialise la connexion à MongoDB"""
import streamlit as st
import time
from streamlit_extras.let_it_rain import rain
from streamlit_extras.metric_cards import style_metric_cards

class information:
    def __init__(self):
        import time
        from streamlit_extras.let_it_rain import rain
        from streamlit_extras.metric_cards import style_metric_cards

        # Configuration de la page
        st.set_page_config(page_title="YeltaCare", page_icon="❤️", layout="centered")

        # Bannière
        st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🩺 Formulaire de Santé</h1>", unsafe_allow_html=True)
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

            genre = st.radio("Genre", ["Homme", "Femme", "Autre"], horizontal=True)

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
            eau = st.slider("💧 Litres d'eau consommés par jour", 0.5, 5.0, 2.0, step=0.1)

            st.subheader("🩺 Antécédents Médicaux")
            antecedents = st.text_area("📜 Antécédents médicaux (ex : diabète, hypertension, etc.)", placeholder="Écrivez ici...")
            fumeur = st.radio("🚬 Fumez-vous ?", ["Non", "Occasionnellement", "Régulièrement"], horizontal=True)
            alcool = st.radio("🍷 Consommez-vous de l'alcool ?", ["Jamais", "Rarement", "Régulièrement"], horizontal=True)

            submit_button = st.form_submit_button("📩 Soumettre")

        if submit_button:
            st.success(f"✅ Profil de santé de {nom} enregistré avec succès !")

            # Calcul de l'IMC
            imc = round(poids / ((taille / 100) ** 2), 2)

            # Affichage dynamique du profil
            st.markdown("<h2 style='text-align: center;'>📊 Votre Profil de Santé</h2>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            col1.metric("📏 Taille", f"{taille} cm")
            col2.metric("⚖️ Poids", f"{poids} kg")
            col3.metric("📌 IMC", f"{imc}")

            col1, col2, col3 = st.columns(3)
            col1.metric("🏃 Activité", activite_physique)
            col2.metric("💤 Sommeil", f"{sommeil}h")
            col3.metric("💧 Eau", f"{eau} L/jour")

            style_metric_cards()

            # --- CONSEILS PERSONNALISÉS ---
            st.markdown("<h3 style='text-align: center;'>💡 Conseils Personnalisés</h3>", unsafe_allow_html=True)

            conseils = []
            if imc < 18.5:
                conseils.append("🍽️ Votre IMC est bas, pensez à une alimentation équilibrée et riche en nutriments.")
            elif imc > 25:
                conseils.append("🏋️ Votre IMC est élevé. Une activité physique régulière et une alimentation saine peuvent aider.")

            if activite_physique in ["Sédentaire", "Légère"]:
                conseils.append("🚶 Essayez d'ajouter plus d'exercice à votre routine quotidienne.")

            if sommeil < 6:
                conseils.append("🌙 Votre sommeil est insuffisant. Essayez d'améliorer votre hygiène de sommeil.")

            if "🍔 Fast-food" in alimentation or "🥤 Boissons sucrées" in alimentation:
                conseils.append("⚠️ Réduire la consommation d'aliments transformés peut améliorer votre santé.")

            if fumeur != "Non":
                conseils.append("🚭 Réduire ou arrêter le tabac est bénéfique pour la santé.")

            if alcool != "Jamais":
                conseils.append("🍷 Une consommation modérée d'alcool est recommandée.")

            for conseil in conseils:
                st.info(conseil)

            # Effet visuel si tout est optimal
            if len(conseils) == 0:
                st.success("🎉 Félicitations ! Votre mode de vie semble équilibré. Continuez ainsi !")
                rain(emoji="🎉", font_size=30, falling_speed=5, animation_length="infinite")

            # --- TEMPS DE CHARGEMENT AVANT REDIRECTION ---
            st.markdown("<h3 style='text-align: center;'>🔄 Création du Profil...</h3>", unsafe_allow_html=True)

            with st.spinner("🔄 Analyse des données en cours..."):
                progress_bar = st.progress(0)
                status_text = st.empty()

                steps = [
                    "📡 Communication avec le serveur...",
                    "📊 Analyse des données...",
                    "🔍 Vérification des antécédents médicaux...",
                    "🔬 Génération du profil santé...",
                    "✅ Finalisation de votre compte..."
                ]

                for i, step in enumerate(steps):
                    status_text.text(step)
                    progress_bar.progress((i + 1) * 20)  # Avance la barre de 20% à chaque étape
                    time.sleep(1)  # Pause pour simuler le chargement

                progress_bar.empty()
                status_text.text("🚀 Redirection en cours...")

                time.sleep(1)  # Attente avant redirection

                # 🚀 Redirection vers la page "principal.py"
                st.switch_page("principal.py")  # Assurez-vous que le fichier principal.py soit dans le même répertoire que votre fichier principal.

