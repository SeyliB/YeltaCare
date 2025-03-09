import streamlit as st
import database
import user
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

collection = database.getCollection("Informations")

def display():

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

def follow_up_screen(document):
    st.header("🌱 Suivi de Santé")
    st.write("Voici le suivi de vos données de santé au fil du temps.")

    # Données d'exemple pour le suivi de santé
    follow_up_data = {
        "Date": ["2023-10-01", "2023-10-02", "2023-10-03", "2023-10-04", "2023-10-05"],
        "Taille (cm)": [170, 170, 170, 170, 170],
        "Poids (kg)": [70, 69.5, 69, 68.5, 68],
        "IMC": [24.22, 23.98, 23.74, 23.50, 23.26],
        "Sommeil (h)": [7, 7.5, 6.5, 8, 7],
        "Stress (/10)": [5, 4, 6, 3, 5],
        "Eau (L)": [2, 2.5, 2, 3, 2.5]
    }

    # Affichage du diagramme en ligne
    follow_up_df = pd.DataFrame(follow_up_data)
    follow_up_df.set_index("Date", inplace=True)

    st.subheader("Évolution des Données de Santé")
    st.line_chart(follow_up_df)

def updater_screen(document):
    st.header("⏳ Actualisateur de Données")
    st.write("Mettez à jour vos données de santé pour un suivi précis.")

    # Formulaire pour mettre à jour les données
    with st.form("update_form"):
        st.subheader("Nouvelles Données")
        date = st.date_input("Date", datetime.today())
        taille_cm = st.number_input("Taille (cm)", value=document.get("taille_cm", 170))
        poids_kg = st.number_input("Poids (kg)", value=document.get("poids_kg", 70))
        sommeil_h = st.number_input("Sommeil (heures)", value=document.get("sommeil_h", 7))
        stress_niveau = st.slider("Niveau de stress (/10)", 0, 10, document.get("stress_niveau", 5))
        eau_L = st.number_input("Eau consommée (L)", value=document.get("eau_L", 2))

        if st.form_submit_button("Mettre à jour"):
            # Mettre à jour le document avec les nouvelles données
            new_data = {
                "date": date.strftime("%Y-%m-%d"),
                "taille_cm": taille_cm,
                "poids_kg": poids_kg,
                "sommeil_h": sommeil_h,
                "stress_niveau": stress_niveau,
                "eau_L": eau_L
            }
            # Ajouter les nouvelles données à l'historique
            if "historique_sante" not in document:
                document["historique_sante"] = []
            document["historique_sante"].append(new_data)

            # Mettre à jour le document dans la base de données
            collection.update_document({"username": user.connected}, document)
            st.success("Données mises à jour avec succès !")