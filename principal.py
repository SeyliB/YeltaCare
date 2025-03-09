import streamlit as st
import streamlit_app as main
import database
import user
import informations
import calendrier
import json
from ai import GeminiAI
import time
import pandas as pd
import plotly.express as px
from datetime import datetime

collection = database.getCollection("Informations")
ai = GeminiAI()
tabs = None

def display():
    global tabs
    document = collection.get_document({"username": user.connected})
    if document != None:

        tabs = st.tabs(
            [
                "📊 Plan de Nutritions et d'Exercices",
                "🌱 Suivi de Santé",
                "⏳ Actualisateur de Données"
            ]
        )

        with tabs[0]:
            plan_screen(document)
        with tabs[1]:
            follow_up_screen(document)
        with tabs[2]:
            updater_screen(document)

def plan_screen(document):
    query = {"username": user.connected}
    data = collection.get_document(query)
    st.set_page_config(page_title="YeltaCare - Santé & Bien-être", layout="wide")

    # Titre principal centré
    st.markdown("<h1 style='text-align: center;'>YeltaCare - Santé & Bien-être</h1>", unsafe_allow_html=True)

    # CSS pour centrer les tabs
    st.markdown(
        """
        <style>
            div[data-testid="stTabs"] {
                display: flex;
                justify-content: center;
            }
            button[data-baseweb="tab"] {
                font-size: 18px !important;
                font-weight: bold !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Création des onglets centrés
    tabs = st.tabs(["🥗 Nutrition"])

    with tabs[0]:  # Nutrition
        st.header("..........................................")

    prompt = (
        "Dépendant des données suivantes correspondant à l'utilisateur " +
        str(data) + ", "
        "je veux que tu remplisses un calendrier allant du lundi au dimanche, de 6h à 20h chaque jour. "
        "Les repas nutritionnels doivent être placés aux heures de repas (petit-déjeuner, déjeuner, dîner). "
        "Les événements doivent être de type 'sport' ou 'nutrition'. "
        "Voici un exemple précis du format attendu : "
        '''[
            {
                "title": "Entraînement Cardio",
                "start": (start_of_week + timedelta(days=1)).strftime("%Y-%m-%dT08:30:00"),
                "end": (start_of_week + timedelta(days=1)).strftime("%Y-%m-%dT10:00:00"),
                "id": 1,
                "type": "sport",  # Type 'sport'
                "day": "Mardi"
            },
            {
                "title": "Yoga Relaxation",
                "start": (start_of_week + timedelta(days=2)).strftime("%Y-%m-%dT11:00:00"),
                "end": (start_of_week + timedelta(days=2)).strftime("%Y-%m-%dT12:00:00"),
                "id": 2,
                "type": "sport",  # Type 'sport'
                "day": "Mercredi"
            },
            {
                "title": "Consultation Nutrition",
                "start": (start_of_week + timedelta(days=3)).strftime("%Y-%m-%dT10:00:00"),
                "end": (start_of_week + timedelta(days=3)).strftime("%Y-%m-%dT11:00:00"),
                "id": 3,
                "type": "nutrition",  # Type 'nutrition'
                "day": "Jeudi"
            },
            {
                "title": "Conseils en Nutrition",
                "start": (start_of_week + timedelta(days=5)).strftime("%Y-%m-%dT14:00:00"),
                "end": (start_of_week + timedelta(days=5)).strftime("%Y-%m-%dT15:00:00"),
                "id": 4,
                "type": "nutrition",  # Type 'nutrition'
                "day": "Samedi"
            }
        ]'''
        "Je veux que tu génères une réponse exactement dans ce format, sans autres informations, et que la réponse soit en JSON valide. et je le veut en format json avec ''' au debut et ''' a la fin mais respect bien les espaces et tout"
    )

    plan_str = ai.generate_text(prompt)

    plan_str = plan_str[8:len(plan_str)-4]

    plan = json.loads(plan_str)

    # st.write(plan)
    # Passer le plan d'événements au module calendrier pour affichage
    calendrier.afficherCalendrierSemaine(plan)

    st.write("Conseil")
    # Générer le conseil du jour
    # st.write(ai.generate_text("Avec ces data je veux que tu lui donne un petit conseil du jour sous la forme d'un petit rappelle de motivation (je veux que le paragraphe de motivation et rien d'autre tu dois le faire en 30-40 mots) " + str(data)))

def show_graph(label, constant, data):
    if len(data) > 0:
        # Création du DataFrame
        df = pd.DataFrame({label: data})

        # Assurer un intervalle de 1 sur l'axe des x
        df["index"] = range(1, len(df) + 1)

        # Création du graphique
        fig = px.line(df, x="index", y=label, markers=True, title=f"Évolution de {label} au fil du temps")
        fig.update_layout(xaxis_title="Entrées dans le temps", yaxis_title=label)

        # Ajout de la ligne horizontale si une constante est fournie
        if constant != None:
            fig.add_hline(y=constant, line_dash="dash", line_color="red", annotation_text=f"{label} Idéal ({constant})", annotation_position="top right")

        # Mise à jour de l'axe des x pour qu'il affiche des entiers
        fig.update_layout(
            xaxis_title="Données dans le temps (Jour)",
            yaxis_title=label,
            xaxis=dict(tickmode="linear", dtick=1)  # Force un espacement de 1 entre les points
        )

        # Affichage du graphique dans Streamlit
        st.plotly_chart(fig)
    else:
        st.error("Données inaccessibles.")

def follow_up_screen(document):

    norms = document.get("norms")
    follow_up = document.get("follow_up")

    keys = {
        "Taille": "taille_cm",
        "Poids": "poids_kg",
        "IMC": "IMC",
        "Sommeil": "sommeil_h",
        "Niveau de stress": "stress_niveau",
        "Eau consommée": "eau_L"
    }

    constants = {}
    datas = {}

    for key, value in keys.items():
        norm = norms.get(value)
        constants[value] = norm
        data = follow_up.get(value)
        datas[value] = data if data != None else []

    st.title("Suivi des données de santé")
    label = st.selectbox("Choisissez une métrique :", list(keys.keys()))
    key = keys.get(label)
    constant = constants.get(key)
    data = datas.get(key)
    show_graph(label, constant, data)

def add_to_follow_up(new):
    query = {"username": user.connected}
    document = collection.get_document(query)
    if document != None:
        follow_up = document.get("follow_up")
        for key, value in new.items():
            list = follow_up.get(key)
            if list != None:
                list.append(value)
                follow_up[key] = list
        new["follow_up"] = follow_up
        modified_count = collection.update_data(query, new)
        return modified_count
    return 0


def updater_screen(document):
    st.header("⏳ Actualisateur de Données")
    st.write("Mettez à jour vos données de santé pour un suivi précis.")

    # Formulaire pour mettre à jour les données
    with st.form("update_form"):
        st.subheader("Nouvelles Données")
        date = st.date_input("Date", datetime.today())
        taille_cm = st.number_input("Taille (cm)", value=document.get("taille_cm", 170))
        poids_kg = st.number_input("Poids (kg)", value=document.get("poids_kg", 70))
        imc = informations.get_imc(taille_cm, poids_kg)
        sommeil_h = st.number_input("Sommeil (heures)", value=document.get("sommeil_h", 7))
        stress_niveau = st.slider("Niveau de stress (/10)", 0, 10, document.get("stress_niveau", 5))
        eau_L = st.number_input("Eau consommée (L)", value=document.get("eau_L", 2))

        if st.form_submit_button("Mettre à jour"):
            # Nouvelles valeurs à mettre à jour
            new = {
                "taille_cm": taille_cm,
                "poids_kg": poids_kg,
                "IMC": imc,
                "sommeil_h": sommeil_h,
                "stress_niveau": stress_niveau,
                "eau_L": eau_L,
            }

            # Mettre à jour le document dans la base de données
            modified_count =  add_to_follow_up(new)

            if modified_count > 0:
                st.success("Données mises à jour avec succès !")
            else:
                st.error("Erreur lors de la mise à jour des données.")