import streamlit as st
import streamlit_app as main
import database
import user
import informations
import time
import pandas as pd
import plotly.express as px
from datetime import datetime

collection = database.getCollection("Informations")
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
    st.header("📊 Plan de Nutritions et d'Exercices")
    st.write("Voici votre horaire hebdomadaire pour la nutrition et les exercices.")

    # Données d'exemple pour le plan de nutrition et d'exercices
    plan_data = {
        "Jour": ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"],
        "Nutrition": [
            "Petit-déjeuner : Œufs, Avocat\nDéjeuner : Poulet grillé, Légumes\nDîner : Poisson, Riz",
            "Petit-déjeuner : Smoothie, Fruits\nDéjeuner : Salade César\nDîner : Steak, Patates douces",
            "Petit-déjeuner : Porridge, Fruits\nDéjeuner : Sandwich, Légumes\nDîner : Poulet, Quinoa",
            "Petit-déjeuner : Yaourt, Granola\nDéjeuner : Soupe, Pain\nDîner : Saumon, Brocoli",
            "Petit-déjeuner : Œufs, Pain complet\nDéjeuner : Salade de Thon\nDîner : Dinde, Légumes",
            "Petit-déjeuner : Pancakes, Fruits\nDéjeuner : Pâtes, Sauce tomate\nDîner : Pizza légère",
            "Petit-déjeuner : Omelette, Légumes\nDéjeuner : Burger sain\nDîner : Sushi"
        ],
        "Exercices": [
            "Course à pied (30 min)",
            "Yoga (45 min)",
            "Musculation (60 min)",
            "Natation (30 min)",
            "Vélo (45 min)",
            "Marche (60 min)",
            "Repos"
        ]
    }

    # Affichage du tableau
    plan_df = pd.DataFrame(plan_data)
    st.dataframe(plan_df)

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