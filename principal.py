import streamlit as st
import pandas as pd

# Charger les données des fichiers CSV
exercices = pd.read_csv("exercices.csv")
nutritions = pd.read_csv("nutritions.csv")

def display():
    # Titre de la page
    st.title("📅 Horaire Hebdomadaire d'Exercices et de Nutrition")

    # Afficher l'horaire des exercices
    st.header("🏋️‍♂️ Exercices")
    st.write("Voici votre programme d'exercices pour la semaine :")

    # Appliquer des couleurs aux cellules du tableau
    def color_exercices(val):
        color = "lightgreen" if "Course" in val else "lightblue" if "Yoga" in val else "lightcoral"
        return f"background-color: {color}"

    styled_exercices = exercices.style.applymap(color_exercices)
    st.dataframe(styled_exercices)

    # Afficher l'horaire de nutrition
    st.header("🍎 Nutrition")
    st.write("Voici votre programme de nutrition pour la semaine :")

    # Appliquer des couleurs aux cellules du tableau
    def color_nutritions(val):
        color = "lightyellow" if "Salade" in val else "lightpink" if "Poulet" in val else "lightcyan"
        return f"background-color: {color}"

    styled_nutritions = nutritions.style.applymap(color_nutritions)
    st.dataframe(styled_nutritions)